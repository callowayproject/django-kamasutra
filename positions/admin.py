from django.contrib import admin
from django.core.urlresolvers import reverse, NoReverseMatch

from positions import settings
from positions.models import Position, PositionContent


class PositionContentInline(admin.TabularInline):
    """Position content inline to manage the content"""
    model = PositionContent
    extra = 0
    max_num = 0
    readonly_fields = ('content_object', 'content_type', 'add_date', )
    fields = ('content_object', 'content_type', 'add_date', 'order', )
    ordering = ('order', )


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'count',  'current_items',
                    'list_eligible_types', 'allow_all_types',)
    search_fields = ('name', 'description')
    filter_horizontal = ('eligible_types',)
    inlines = [PositionContentInline]

    def list_eligible_types(self, obj):
        """Display a list of the eligible types to display on the change list.

        This list is limited to only 5 items in order not to clutter up the
        admin change list.

        """
        items = []
        eligible_types = obj.eligible_types.all()
        for content_type in eligible_types[:5]:
            items.append(u'<li>{}.{}</li>'.format(content_type.app_label, content_type.model))

        if eligible_types.count() > 5:
            items.append(u'<br/>and {} more'.format(eligible_types.count() - 5))

        return u'<ul>{}</ul>'.format(u''.join(items))
    list_eligible_types.allow_tags = True
    list_eligible_types.short_description = 'Eligible Types'

    def current_items(self, obj):
        """Display a list of the current position content

        Each item will be wrapped in a admin change form link if the item
        is editable via the admin. This list also only shows the first 5
        items in order not to clutter up the admin change list.

        A horizontal rule is placed between returned objects and
        overlap objects.

        """
        items = []
        position_contents = obj.positioncontent_set.all()
        for i, pobj in enumerate(position_contents[:5]):
            item = unicode(pobj.content_object)
            try:
                reverse_name = u'admin:{}_{}_change'.format(
                    pobj.content_type.app_label,
                    pobj.content_type.model)
                item_link = reverse(reverse_name, args=[pobj.content_object.id])
                item = u'<a href="{}">{}</a>'.format(
                    item_link, unicode(pobj.content_object))
            except (NoReverseMatch, AttributeError):
                pass
            items.append(u'<li>{}</li>'.format(item))
            if i+1 == obj.count:
                items.append(u'<hr style="background-color:#a2a2a2;"/>')

        if position_contents.count() > 5:
            items.append(u'<br/> and {} more'.format(
                position_contents.count() - 5))

        return u'<ul>{}</ul>'.format(''.join(items))
    current_items.allow_tags = True


class PositionContentAdmin(admin.ModelAdmin):
    list_display = ('position', 'content_object', 'order', 'add_date',)


admin.site.register(Position, PositionAdmin)
admin.site.register(PositionContent, PositionContentAdmin)
