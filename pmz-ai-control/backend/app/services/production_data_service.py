from sqlalchemy.orm import Session

from app.models.materials import Material


def get_summary(db: Session) -> dict:
    return {"materials": db.query(Material).count()}
