from django.contrib import admin
from django.utils.html import format_html
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_badge', 'title', 'read_badge', 'created_at']
    list_filter = ['notif_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    actions = ['mark_as_read']

    def type_badge(self, obj):
        colors = {
            'application':       ('#0d6efd', '📋 Application'),
            'message':           ('#6f42c1', '💬 Message'),
            'mission_accepted':  ('#198754', '✔ Accepted'),
            'mission_completed': ('#fd7e14', '🏁 Completed'),
        }
        color, label = colors.get(obj.notif_type, ('#6c757d', obj.notif_type))
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, label
        )
    type_badge.short_description = 'Type'

    def read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color:#198754;font-weight:600">✔ Read</span>')
        return format_html('<span style="color:#dc3545;font-weight:600">● Unread</span>')
    read_badge.short_description = 'Status'

    @admin.action(description='✔ Mark selected notifications as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
