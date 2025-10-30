from django.apps import AppConfig


class ScoutingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scouting'
    verbose_name = 'Scouting'

    def ready(self):
        """Import signals when app is ready."""
        import scouting.signals  # noqa
