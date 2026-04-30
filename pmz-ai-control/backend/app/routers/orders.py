from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.orders import Order
from app.services.ai_service import find_order
from app.services.orders_service import create_order, get_order, list_orders, update_order

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderCreate(BaseModel):
    order_number: str
    customer_order: str | None = None
    plant: str | None = None
    quantity: float | None = None
    unit: str | None = None
    contract_number: str | None = None
    required_date: date | None = None
    status: str | None = None


class OrderUpdate(BaseModel):
    customer_order: str | None = None
    plant: str | None = None
    quantity: float | None = None
    unit: str | None = None
    contract_number: str | None = None
    required_date: date | None = None
    status: str | None = None


@router.get("/")
def orders(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    plant: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    items = list_orders(db, limit=limit, offset=offset, status=status, plant=plant)
    return {"items": [serialize(x) for x in items], "limit": limit, "offset": offset}


@router.post("/")
def add_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not payload.order_number.strip():
        return {"error": "order_number is required"}
    x = create_order(db, **payload.model_dump())
    return {"id": x.id, "order_number": x.order_number}


@router.patch("/{order_number}")
def patch_order(order_number: str, payload: OrderUpdate, db: Session = Depends(get_db)):
    x = update_order(db, order_number=order_number, payload=payload.model_dump(exclude_none=True))
    if not x:
        return {"error": "not found"}
    return serialize(x)


@router.get("/{order_number}/card")
def order_card(order_number: str, db: Session = Depends(get_db)):
    core = find_order(db, order_number)
    if not core:
        raise HTTPException(status_code=404, detail="Order not found")
    order = db.query(Order).filter(Order.order_number == order_number).first()
    return {
        "order": core,
        "contract_number": order.contract_number,
        "customer_order": order.customer_order,
    }


@router.get("/{order_number}")
def order_details(order_number: str, db: Session = Depends(get_db)):
    x = get_order(db, order_number)
    if not x:
        return {"error": "not found"}
    return serialize(x)


def serialize(x: Order) -> dict:
    return {
        "id": x.id,
        "order_number": x.order_number,
        "customer_order": x.customer_order,
        "plant": x.plant,
        "quantity": float(x.quantity or 0),
        "unit": x.unit,
        "contract_number": x.contract_number,
        "required_date": str(x.required_date) if x.required_date else None,
        "status": x.status,
    }
