"""Auditlog registration for accounts app models."""

from auditlog.registry import auditlog

from accounts.models import CustomUser

# Register CustomUser model for audit logging
auditlog.register(CustomUser)
