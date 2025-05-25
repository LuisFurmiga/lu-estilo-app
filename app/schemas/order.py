# lu-estilo-app/app/schemas/order.py
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.order_item import OrderItemRead

class OrderItem(BaseModel):
    product_id: int = Field(..., json_schema_extra={"example": 1})
    quantity: int = Field(..., json_schema_extra={"example": 10})

class OrderCreate(BaseModel):
    client_id: int = Field(..., json_schema_extra={"example": 1})
    items: List[OrderItem]

class OrderUpdate(BaseModel):
    status: Optional[str] = Field(..., json_schema_extra={"example": "enviado"})

class OrderRead(BaseModel):
    id: int
    client_id: int = Field(..., json_schema_extra={"example": 1})
    status: str = Field(..., json_schema_extra={"example": "pendente"})
    created_at: datetime = Field(..., json_schema_extra={"example": "2025-12-12"})
    items: List[OrderItemRead] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "client_id": 1,
                "status": "pendente",
                "created_at": "2025-12-12T00:00:00",
                "items": [
                    {
                        "id": 1,
                        "order_id": 1,
                        "product_id": 1,
                        "quantity": 10
                    }
                ]
            }
        }
    )
