# lu-estilo-app/app/models/order.py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.order_item import OrderItem

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    status = Column(String, default="pendente")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
