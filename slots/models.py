import datetime
from django.db import models
from django.db.models import Count, F
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache

from slots import settings as slot_settings
from slots import utils

class SlotManager(models.Manager):
    
    def add_object(self, slot, obj, position=1):
        """
        Add an object to a slot.
        """
        # check to make sure position is within the slot count
        if not position in range(1, slot.count+1):
            position = 1

        ctype = ContentType.objects.get_for_model(obj)
        if not self.is_applicable(slot, obj):
            return False
        
        # Create the new SlotContent object, force uniquness.
        try:
            SlotContent._default_manager.get(slot__pk=slot.pk, 
                content_type__pk=ctype.pk, object_id=str(obj.id))
            return False
        except SlotContent.DoesNotExist:
            new_obj = SlotContent._default_manager.create(slot=slot, content_type=ctype, 
                object_id=obj.pk, order=position, add_date=datetime.datetime.now())

            
        SlotContent.objects.reorder(slot, new_obj)
        SlotContent.objects.prune(slot)
        SlotContent.objects.rebuild_cache(slot)
        
        return True
            
    def remove_object(self, slot, obj):
        """
        Remove an object from a slot.
        """
        ctype = ContentType.objects.get_for_model(obj)
        try:
            item = SlotContent._default_manager.get(slot=slot, content_type=ctype, object_id=str(obj.pk))
        except SlotContent.DoesNotExist:
            return False
            
        SlotContent.objects.reorder(slot, item, is_new=False)
        item.delete()
        SlotContent.objects.rebuild_cache(slot)
    
    def get_content(self, slot, count=None, as_contenttype=True):
        """
        Gets the content for the slot given.
            - Even though content is cached, when specifing a custom
                count the items will not be re-cached automatically
                when removing or adding objects to specified slot. See
                SlotContentManager.rebuild_cache for more inforamation.
        """
        # Get the number of items that are going to be returned.
        num = slot.count
        ex = ''
        if isinstance(count, int):
            num = count
            if num != slot.count:
                ex = 'custom'
            
        # Get the cache key.
        key = utils.get_cache_key(slot, ex)
        items = cache.get(key)
        if items:
            return items
        
        # Get the items
        items = SlotContent._default_manager.filter(
            slot=slot).order_by('order')[:num]
            
        # If supplied, return the content objects.
        if as_contenttype:
            items = [item.content_object for item in items if item.content_object]
            
        # Set the cache.
        cache.set(key, items, slot_settings.CACHE_TIMEOUT)
        
        return items
            
    def contains_object(self, slot, obj):
        ctype = ContentType.objects.get_for_model(obj)
        
        try:
            slot.slotcontent_set.get(content_type__pk=ctype.pk, object_id=str(obj.pk))
        except SlotContent.DoesNotExist:
            return False
            
        return True
        
        
    def get_applicable(self, obj):
        """
        Gets the slots that the object can be assigned.
        """
        ctype = ContentType.objects.get_for_model(obj)
        slots = self.filter(eligible_types__in=[ctype,])
        # If no slots found with eligible_type of supplied obj, then
        # check for slots that allow all types.
        if not slots:
            slots = self.filter(allow_all_types=True)
        return slots
        
    def is_applicable(self, slot, obj):
        """
        Check to make sure object can be assigned to a slot.
        """
        ctype = ContentType.objects.get_for_model(obj)
        items = self.filter(pk=slot.pk, eligible_types__in=[ctype,])
        if items:
            return True
        return False


class Slot(models.Model):
    """
    Slot model
        The need to be able to position something somewhere.
    """
    name = models.SlugField(_('Name (slug)'), unique=True,
        help_text=_('Name of the slot, must only contain alpha numeric characters.'))
    is_static = models.BooleanField(_('Static'), default=True, 
        help_text=_('Defines if slot is static. ie: not generated dynamically.'))
    count = models.PositiveIntegerField(_('Count'), default=1,
        help_text=_('The number of items to return when getting the slot content.'))
    eligible_types = models.ManyToManyField(ContentType, verbose_name=_('Eligible Types'), null=True, blank=True, 
        help_text=_('The types of content that this slot can contain. Select none for allowing all content types.'))
    allow_all_types = models.BooleanField(_('Allow all Content Types'), default=False, 
        help_text=_('Select this check box if this slot should allow all types of content.'))
    description = models.TextField(_('Description'), blank=True)
    sites = models.ManyToManyField(Site, verbose_name=_(u'Sites'), null=True, blank=True,
        help_text=_('The site where this slot will be available. Select none for this slot to be available on all sites.'))
    
    objects = SlotManager()
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name
        
        
class SlotContentManager(models.Manager):
    def rebuild_cache(self, slot):
        """
        Rebuilds the item cache for the specified slot and its slot count.
            - Will not re-cache custom counts sent to SlotManager.get_content
        """
        key = '%s.%s_items.%s' % (slot_settings.CACHE_PREFIX, slot.name, slot.count)
        cache.set(key, Slot.objects.get_content(slot), 
            slot_settings.CACHE_TIMEOUT)
        
    def prune(self, slot):
        """
        Trim the amount of items in the slot.
        """
        items = self.filter(slot=slot).order_by('order')
        if len(items) > slot.count + slot_settings.CONTENT_OVERLAP_COUNT:
            items = items[(slot.count + slot_settings.CONTENT_OVERLAP_COUNT):]
            items.delete()

        self.rebuild_cache(slot)
        
    def reorder(self, slot, new_or_old_content, is_new=True):
        """
        Reorder the content after a new content object is removed or added.
        """
        for item in self.filter(slot=slot).order_by('order'):
            if item != new_or_old_content:
                if is_new:
                    if item.order >= new_or_old_content.order:
                        item.order += 1
                else:
                    if item.order > new_or_old_content.order:
                        item.order -= 1
                
                item.save()


class SlotContent(models.Model):
    """
    Slot Content
        Holds the content assigned to a particular slot.
    """
    slot = models.ForeignKey(Slot, verbose_name=_('Slot'), 
        help_text=_('The slot where this object will be shown.'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type of the object.'),
        help_text=_('Type of this object.'))
    object_id = models.CharField(_('Object ID'), max_length=255, 
        help_text=_('The ID/PK of the object.'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(_('Order'), default=1,
        help_text=_('The order of the object.'))
    add_date = models.DateTimeField(_('Date Added'), default=datetime.datetime.now)
    
    objects = SlotContentManager()
    
    class Meta:
        ordering = ['slot__name', 'order', '-add_date']
    
    def __unicode__(self):
        return '%s - %s' % (self.slot.name, self.content_object)