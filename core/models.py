from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    """Store user notifications for important system events."""

    TYPE_INJURY = 'INJURY'
    TYPE_REPORT = 'REPORT'
    TYPE_GENERAL = 'GENERAL'

    TYPE_CHOICES = [
        (TYPE_INJURY, 'Lesão registrada'),
        (TYPE_REPORT, 'Relatório completado'),
        (TYPE_GENERAL, 'Geral'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Destinatário',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        verbose_name='Remetente',
        null=True,
        blank=True,
    )
    notification_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES,
        default=TYPE_GENERAL,
    )
    title = models.CharField('Título', max_length=200)
    message = models.TextField('Mensagem')
    is_read = models.BooleanField('Lida', default=False)
    link = models.CharField('Link', max_length=500, blank=True)

    # Generic relation to any model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f'{self.title} - {self.recipient.email}'

    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read', 'updated_at'])

    def type_badge_class(self):
        """Return Tailwind classes for notification type badge."""
        mapping = {
            self.TYPE_INJURY: 'bg-red-500/20 text-red-300 border border-red-400/30',
            self.TYPE_REPORT: 'bg-blue-500/20 text-blue-300 border border-blue-400/30',
            self.TYPE_GENERAL: 'bg-slate-700 text-slate-200 border border-slate-600/40',
        }
        return mapping.get(self.notification_type, 'bg-slate-700 text-slate-200 border border-slate-600/40')
