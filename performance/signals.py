from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Notification
from performance.models import InjuryRecord


@receiver(post_save, sender=InjuryRecord)
def create_injury_notification(sender, instance, created, **kwargs):
    """Create notification when a new injury record is created."""
    if created:
        # Notify the user who created it
        Notification.objects.create(
            recipient=instance.created_by,
            sender=instance.created_by,
            notification_type=Notification.TYPE_INJURY,
            title='Nova lesão registrada',
            message=f'Lesão de {instance.athlete.name} foi registrada: {instance.get_injury_type_display()} - {instance.get_body_part_display()}',
            link=f'/performance/injuries/{instance.id}/',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
