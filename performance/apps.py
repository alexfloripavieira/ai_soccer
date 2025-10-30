from django.apps import AppConfig


class PerformanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'performance'
    verbose_name = 'Performance'

    def ready(self):
        """Import signals and auditlog registration when app is ready."""
        import performance.signals  # noqa
        import performance.auditlog  # noqa
