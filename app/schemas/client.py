# lu-estilo-app/app/schemas/client.py
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator, Field
import re

def validar_cpf(cpf: str) -> bool:
    # Remove não dígitos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se tem 11 dígitos e se todos são iguais
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Cálculo dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i+1) - j) for j in range(i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False

    return True

class ClientBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Ameixa"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ameixa@email.com"})
    cpf: constr(min_length=11, max_length=11) = Field(..., json_schema_extra={"example": "CPF VALIDO!"})

    @field_validator("cpf")
    @classmethod
    def cpf_valido(cls, v):
        if not validar_cpf(v):
            raise ValueError("CPF inválido")
        return v

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(..., json_schema_extra={"example": "Ameixa 2.0"})
    email: Optional[EmailStr] = Field(..., json_schema_extra={"example": "ameixa2.0@email.com"})
    cpf: Optional[constr(min_length=11, max_length=11)] = Field(..., json_schema_extra={"example": "CPF VALIDO!"})

class ClientRead(ClientBase):
    id: int = Field(..., json_schema_extra={"example": "1"})

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Ameixa",
                "email": "ameixa@email.com",
                "cpf": "CPF VALIDO!"
            }
        }
    )
