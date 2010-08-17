from django.contrib import admin
from django.core.urlresolvers import reverse

from positions import settings
from positions.models import Position, PositionContent

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'count', 
        'allow_all_types', 'change_content_order')
    search_fields = ('name', 'description')
    filter_horizontal = ('eligible_types',)

    def change_content_order(self, obj):
        return '<a href="%s">Change Order</a>' % reverse('positions_ordercontent', args=(str(obj.pk),))
    change_content_order.short_description = ''
    change_content_order.allow_tags = True


class PositionContentAdmin(admin.ModelAdmin):
    list_display = ('position', 'content_object', 'order', 'add_date',)


admin.site.register(Position, PositionAdmin)
admin.site.register(PositionContent, PositionContentAdmin)