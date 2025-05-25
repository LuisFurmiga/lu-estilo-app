# lu-estilo-app/app/schemas/order_item.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.schemas.product import ProductRead

class OrderItemRead(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    order_id: int = Field(..., json_schema_extra={"example": 1})
    product_id: int = Field(..., json_schema_extra={"example": 1})
    quantity: int = Field(..., json_schema_extra={"example": 10})
    product: Optional[ProductRead]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "order_id": 1,
                "product_id": 1,
                "quantity": 10,
                "product": {
                    "id": 1,
                    "description": "Dog Chow",
                    "price": 19.99,
                    "barcode": "7891000244722",
                    "section": "Pet Shop",
                    "stock": 79,
                    "expiration_date": "2025-12-12",
                    "image": "https://www.purina.com/.netlify/images?url=https%3A%2F%2Flive.purina.com%2Fsites%2Fdefault%2Ffiles%2Fproducts%2F2024-01%2Fdc_softbites_chkn_72oz_00017800101059_vanity-hero_1000x1000.jpg",
                    "available": True
                }
            }
        }
    )
