"""Auditlog registration for scouting app models."""

from auditlog.registry import auditlog

from scouting.models import ScoutedPlayer, ScoutingReport

# Register scouting models for audit logging
auditlog.register(ScoutedPlayer)
auditlog.register(ScoutingReport)
