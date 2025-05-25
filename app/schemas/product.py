# lu-estilo-app/app/schemas/product.py
from pydantic import BaseModel, ConfigDict, conint, confloat, Field
from typing import Optional
from datetime import date

link_example = "https://www.purina.com/.netlify/images?url=https%3A%2F%2Flive.purina.com%2Fsites%2Fdefault%2Ffiles%2Fproducts%2F2024-01%2Fdc_softbites_chkn_72oz_00017800101059_vanity-hero_1000x1000.jpg"

class ProductBase(BaseModel):
    description: str  = Field(..., json_schema_extra={"example": "Dog Chow"})
    price: confloat(ge=0) = Field(..., json_schema_extra={"example": 19.99})
    barcode: str = Field(..., json_schema_extra={"example": "7891000244722"})
    section: str = Field(..., json_schema_extra={"example": "Pet Shop"})
    stock: conint(ge=0) = Field(..., json_schema_extra={"example": 99})
    expiration_date: Optional[date] = Field(..., json_schema_extra={"example": "2025-12-12"})
    image: Optional[str] = Field(..., json_schema_extra={"example": link_example})
    available: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    description: Optional[str] = Field(..., json_schema_extra={"example": "Dog Chow"})
    price: Optional[float] = Field(..., json_schema_extra={"example": 19.99})
    barcode: Optional[str] = Field(..., json_schema_extra={"example": "7891000244722"})
    section: Optional[str] = Field(..., json_schema_extra={"example": "Pet Shop"})
    stock: Optional[int] = Field(..., json_schema_extra={"example": 99})
    expiration_date: Optional[date] = Field(..., json_schema_extra={"example": "2025-12-12"})
    image: Optional[str] = Field(..., json_schema_extra={"example": link_example})
    available: Optional[bool] = Field(..., json_schema_extra={"example": True})

class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "description": "Dog Chow",
                "price": 19.99,
                "barcode": "7891000244722",
                "section": "Pet Shop",
                "stock": 79,
                "expiration_date": "2025-12-12",
                "image": link_example,
                "available": True
            }
        }
    )
