from django.contrib import admin
from slots.models import Slot, SlotContent

class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_static', 'count', 'change_content_order')
    search_fieldsets = ('name', 'description', )
    list_per_page = 25
    filter_horizontal = ('eligible_types','sites',)

    def change_content_order(self, obj):
        return '<a href="/admin/slots/slotmanagement/%s/%s/">Change</a>' % (str(obj.pk), 'order_content')
    change_content_order.short_description = 'Change Order'
    change_content_order.allow_tags = True


class SlotContentAdmin(admin.ModelAdmin):
    list_display = ('slot', 'content_object', 'order', 'add_date', )
    list_per_page = 25


admin.site.register(Slot, SlotAdmin)
admin.site.register(SlotContent, SlotContentAdmin)