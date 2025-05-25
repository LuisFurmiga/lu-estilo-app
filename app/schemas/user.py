# lu-estilo-app/app/schemas/user.py
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Ameixa"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ameixa@email.com"})

class UserCreate(UserBase):
    password: str = Field(..., json_schema_extra={"example": "123456"})

class UserLogin(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "ameixa@email.com"})
    password: str = Field(..., json_schema_extra={"example": "123456"})

class UserRead(UserBase):
    id: int
    is_admin: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Ameixa",
                "email": "ameixa@email.com",
                "password": "123456",
                "is_admin": False
            }
        }
    )
