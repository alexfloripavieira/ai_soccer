from django.apps import AppConfig


class PerformanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'performance'
    verbose_name = 'Performance'

    def ready(self):
        """Import signals when app is ready."""
        import performance.signals  # noqa
