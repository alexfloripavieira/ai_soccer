from django.apps import AppConfig


class BusinessConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "business"

    def ready(self):
        """Import auditlog registration when app is ready."""
        import business.auditlog  # noqa
