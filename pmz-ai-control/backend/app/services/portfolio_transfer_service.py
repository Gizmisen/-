from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio
from app.models.master_data import PortfolioTransfer


def preview_transfers(db: Session, limit: int = 200) -> list[PortfolioTransfer]:
    batch_id = str(uuid4())
    rows = db.query(OrderPortfolio).filter((OrderPortfolio.order_status == "open") | (OrderPortfolio.order_status == "в работе")).limit(limit).all()
    out = []
    for r in rows:
        rec = PortfolioTransfer(
            transfer_batch_id=batch_id,
            source_portfolio_id=r.id,
            plant=r.plant,
            material_code=r.material_code,
            material_name=r.material_name,
            qty=float(r.qty or 0),
            hours=float(r.planned_qty or 0),
            delivery_date=r.planned_delivery_date,
            transfer_type="add",
            planning_variant="УТОЧНЁННАЯ ЗАЯВКА_ПЕРЕНОС",
            status="в работу",
        )
        db.add(rec)
        out.append(rec)
    db.commit()
    return out


def confirm_transfers(db: Session, batch_id: str) -> int:
    return db.query(PortfolioTransfer).filter(PortfolioTransfer.transfer_batch_id == batch_id).count()


def delete_current_transfers(db: Session) -> int:
    q = db.query(PortfolioTransfer)
    count = q.count()
    q.delete()
    db.commit()
    return count
