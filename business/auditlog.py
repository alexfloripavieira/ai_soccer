"""Auditlog registration for business app models."""

from auditlog.registry import auditlog

from business.models import Club, FinancialRecord, Revenue

# Register business models for audit logging
auditlog.register(Club)
auditlog.register(FinancialRecord)
auditlog.register(Revenue)
