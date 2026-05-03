from django.contrib import admin
from django.utils.html import format_html
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'mission', 'preview', 'read_badge', 'sent_at']
    list_filter = ['is_read', 'sent_at']
    search_fields = ['sender__username', 'mission__title', 'content']
    readonly_fields = ['sent_at']
    list_per_page = 30
    date_hierarchy = 'sent_at'

    def preview(self, obj):
        text = obj.content[:60] + '…' if len(obj.content) > 60 else obj.content
        return text
    preview.short_description = 'Message'

    def read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color:#198754;font-weight:600">✔ Read</span>')
        return format_html('<span style="color:#ffc107;font-weight:600">● Unread</span>')
    read_badge.short_description = 'Status'
