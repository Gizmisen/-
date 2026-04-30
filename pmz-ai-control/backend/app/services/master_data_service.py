from sqlalchemy.orm import Session

from app.models.master_data import Customer, Plant, PortfolioPlanningVariant, WorkCenter


def list_work_centers(db: Session, limit: int = 200):
    return db.query(WorkCenter).order_by(WorkCenter.id.desc()).limit(limit).all()


def create_work_center(db: Session, payload: dict) -> WorkCenter:
    row = WorkCenter(**payload)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_customers(db: Session, limit: int = 200):
    return db.query(Customer).order_by(Customer.id.desc()).limit(limit).all()


def create_customer(db: Session, payload: dict) -> Customer:
    row = Customer(**payload)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_plants(db: Session, limit: int = 200):
    return db.query(Plant).order_by(Plant.id.desc()).limit(limit).all()


def create_plant(db: Session, payload: dict) -> Plant:
    exists = db.query(Plant).filter(Plant.plant_code == payload["plant_code"]).first()
    if exists:
        return exists
    row = Plant(**payload)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_variants(db: Session, limit: int = 200):
    return db.query(PortfolioPlanningVariant).order_by(PortfolioPlanningVariant.id.desc()).limit(limit).all()


def create_variant(db: Session, payload: dict) -> PortfolioPlanningVariant:
    exists = db.query(PortfolioPlanningVariant).filter(PortfolioPlanningVariant.variant_code == payload["variant_code"]).first()
    if exists:
        return exists
    row = PortfolioPlanningVariant(**payload)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
