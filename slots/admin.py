from django.contrib import admin
from slots.models import Slot

class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_static', 'count', )
    search_fieldsets = ('name', 'description', )
    list_per_page = 25
    filter_horizontal = ('eligible_types','sites',)
    

admin.site.register(Slot, SlotAdmin)