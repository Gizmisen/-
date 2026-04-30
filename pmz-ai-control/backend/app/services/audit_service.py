from sqlalchemy.orm import Session

from app.models.audit import AuditLog


def write_audit(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    new_value: dict | None = None,
    old_value: dict | None = None,
    comment: str | None = None,
    user_id: int | None = None,
) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_value,
            comment=comment,
        )
    )
    db.commit()
