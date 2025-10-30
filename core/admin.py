from django.contrib import admin

from core.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""

    list_display = [
        'title',
        'recipient',
        'notification_type',
        'is_read',
        'created_at',
    ]
    list_filter = [
        'notification_type',
        'is_read',
        'created_at',
    ]
    search_fields = [
        'title',
        'message',
        'recipient__email',
        'recipient__first_name',
        'recipient__last_name',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Informações principais', {
            'fields': ('recipient', 'sender', 'notification_type', 'title', 'message'),
        }),
        ('Detalhes', {
            'fields': ('is_read', 'link', 'content_type', 'object_id'),
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
