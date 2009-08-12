from django.contrib import admin
from slots.models import Slot, SlotContent

class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_static', 'count', )
    search_fieldsets = ('name', 'description', )
    list_per_page = 25
    filter_horizontal = ('eligible_types','sites',)


class SlotContentAdmin(admin.ModelAdmin):
    list_display = ('slot', 'content_object', 'order', 'add_date', )
    list_per_page = 25


admin.site.register(Slot, SlotAdmin)
admin.site.register(SlotContent, SlotContentAdmin)