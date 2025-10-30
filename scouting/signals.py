from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Notification
from scouting.models import ScoutingReport


@receiver(post_save, sender=ScoutingReport)
def create_report_notification(sender, instance, created, **kwargs):
    """Create notification when a new scouting report is created."""
    if created:
        # Notify the user who created it
        Notification.objects.create(
            recipient=instance.created_by,
            sender=instance.created_by,
            notification_type=Notification.TYPE_REPORT,
            title='Novo relatório de scouting',
            message=f'Relatório de {instance.player.name} foi completado. Avaliação geral: {instance.overall_score():.1f}/10',
            link=f'/scouting/reports/{instance.id}/',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
