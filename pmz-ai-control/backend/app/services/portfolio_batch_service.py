from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio
from app.models.master_data import PortfolioBatchImportRow
from app.services.audit_service import write_audit


def preview_batch(db: Session, file_import_id: int, limit: int = 500) -> list[PortfolioBatchImportRow]:
    return db.query(PortfolioBatchImportRow).filter(PortfolioBatchImportRow.file_import_id == file_import_id).order_by(PortfolioBatchImportRow.id.asc()).limit(limit).all()


def confirm_batch(db: Session, file_import_id: int, author: str = "system") -> dict:
    rows = db.query(PortfolioBatchImportRow).filter(PortfolioBatchImportRow.file_import_id == file_import_id).all()
    created = 0
    for r in rows:
        if r.validation_status and r.validation_status.lower() == "error":
            continue
        db.add(OrderPortfolio(
            period=f"{r.year:04d}-{r.month:02d}" if r.year and r.month else "1970-01",
            plant=r.plant,
            customer_name=r.customer_name,
            planning_variant=r.planning_variant,
            order_number=r.order_number or "",
            order_open_date=r.order_open_date,
            material_code=r.material_code,
            material_name=r.material_name,
            qty=r.variant_qty,
            planned_delivery_date=r.delivery_date,
            order_status=r.status,
            note=r.note,
        ))
        created += 1
    db.commit()
    write_audit(db, action="portfolio_batch_confirm", entity_type="portfolio", new_value={"file_import_id": file_import_id, "created": created, "author": author})
    return {"created": created, "rows": len(rows)}
