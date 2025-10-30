"""Auditlog registration for performance app models."""

from auditlog.registry import auditlog

from performance.models import Athlete, InjuryRecord, TrainingLoad

# Register performance models for audit logging
auditlog.register(Athlete)
auditlog.register(TrainingLoad)
auditlog.register(InjuryRecord)
