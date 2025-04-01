from django.contrib import admin
from .models import Category, Navigation, UserNote, UserSettings

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order', 'id')

@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'url', 'description')
    ordering = ('category', 'order', 'id')

@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_preview', 'created_at', 'updated_at')
    list_filter = ('user',)
    search_fields = ('content',)
    ordering = ('-updated_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '内容预览'

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'layout', 'updated_at')
    list_filter = ('theme', 'layout')
    search_fields = ('user__username',)
