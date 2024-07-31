from django.contrib import admin

from .models import Placement


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'content',
        'image',
        'video_link',
        'author',
        'created_at',
        'updated_at',
        'body_part',
    ]
    list_display = [
        'title',
        'author'
    ]
    list_filter = ['body_part', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
