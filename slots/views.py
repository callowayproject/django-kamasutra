from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.decorators.cache import cache_page
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from slots.models import Slot, SlotContent


def get_admin_url(obj):
    """
    Returns the admin URL for the specified object, so that add and remove
    requests may redirect back to the object for which the operation was
    performed.
    """
    return "/admin/%s/%s/%s" % (obj._meta.app_label,
            obj._meta.module_name, obj.id)
 
def add(request, slotname, type, id):
    try:
        slot = Slot.objects.get(name__iexact=slotname)
    except Slot.DoesNotExist:
        raise Http404
        
    c = ContentType.objects.get(id=type)
    obj = c.get_object_for_this_type(id=id)
    if slot not in Slot.objects.get_applicable(obj):
        return HttpResponseForbidden("The object cannot be added to this slot.")
    
    Slot.objects.add_object(slot, obj)
    
    return HttpResponseRedirect(get_admin_url(obj))

add = staff_member_required(add)

def remove(request, slotname, type, id):
    """
    Resolves the object by the specified content type and id, and removes it
    from the specified Slot if it has already been added.
    """
    try:
        slot = Slot.objects.get(name__iexact=slotname)
    except Slot.DoesNotExist:
        raise Http404
        
    c = ContentType.objects.get(id=type)
    obj = c.get_object_for_this_type(id=id)

    if slot not in Slot.objects.get_applicable(obj):
        return HttpResponseForbidden("The object cannot be added to this slot.")
    
    Slot.objects.remove_object(slot=slot, obj=obj)
    
    return HttpResponseRedirect(get_admin_url(obj))

remove = staff_member_required(remove)
