from django.contrib import admin
from django.core.urlresolvers import reverse

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
    list_display = ('name', 'description', 'count', 'allow_all_types', )
    search_fields = ('name', 'description')
    filter_horizontal = ('eligible_types',)
    inlines = [PositionContentInline]


class PositionContentAdmin(admin.ModelAdmin):
    list_display = ('position', 'content_object', 'order', 'add_date',)


admin.site.register(Position, PositionAdmin)
admin.site.register(PositionContent, PositionContentAdmin)
