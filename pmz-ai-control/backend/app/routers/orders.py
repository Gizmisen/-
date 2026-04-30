from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.orders import Order
from app.services.ai_service import find_order

router = APIRouter(prefix="/orders", tags=["orders"])


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
