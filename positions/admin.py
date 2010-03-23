from django.contrib import admin
from positions.models import Position, PositionContent

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'count', 'change_content_order')
    search_fieldsets = ('name', 'description', )
    list_per_page = 25
    filter_horizontal = ('eligible_types','sites',)

    def change_content_order(self, obj):
        return '<a href="/position_management/%s/%s/">Change</a>' % (str(obj.pk), 'order_content')
    change_content_order.short_description = 'Change Order'
    change_content_order.allow_tags = True


class PositionContentAdmin(admin.ModelAdmin):
    list_display = ('position', 'content_object', 'order', 'add_date', )
    list_per_page = 25


admin.site.register(Position, PositionAdmin)
admin.site.register(PositionContent, PositionContentAdmin)