# lu-estilo-app/app/services/order_service.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    section: Optional[str] = None,
    order_id: Optional[int] = None,
    status: Optional[str] = None,
    client_id: Optional[int] = None,
) -> List[Order]:
    query = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    )

    if order_id is not None:
        query = query.filter(Order.id == order_id)
    if status is not None:
        query = query.filter(Order.status == status)
    if client_id is not None:
        query = query.filter(Order.client_id == client_id)
    if start_date and end_date:
        query = query.filter(and_(Order.created_at >= start_date, Order.created_at <= end_date))
    if section:
        query = query.join(Order.items).join(Product).filter(Product.section == section)

    return query.offset(skip).limit(limit).all()
