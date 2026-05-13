from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class ProductStatus(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    INDISPONIVEL = "INDISPONIVEL"

class ProductBase(BaseModel):
    codigo: str = Field(..., min_length=1)
    nome: str = Field(..., min_length=1)
    preco: float = Field(..., gt=0)
    status: ProductStatus

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    data_cadastro: datetime
    email_admin: EmailStr