from typing import Dict, Any
from sqlalchemy.orm import Session
from clincode_api.db.models import AuditLog


def log_audit_event(
    db: Session,
    actor: str,
    action: str,
    resource_type: str,
    resource_id: str,
    detail: Dict[str, Any] = None
) -> AuditLog:
    """Logs an immutable healthcare audit log record."""
    entry = AuditLog(
        actor=actor,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail or {}
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
