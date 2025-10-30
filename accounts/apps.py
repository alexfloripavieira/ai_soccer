from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        """Import auditlog registration when app is ready."""
        import accounts.auditlog  # noqa
