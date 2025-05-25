# lu-estilo-app/app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.user import UserRead
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import *
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/", 
    summary="Listar produtos",
    description="Retorna todos os produtos cadastrados com suporte a paginação e filtros por categoria (seção), preço e disponibilidade.",
    response_model=List[ProductRead]
)
def list_products(
    skip: int = 0, 
    limit: int = 10, 
    section: str = None, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    return get_products(db, skip, limit, section)

@router.post(
    "/", 
    summary="Criar novo produto",
    description="Cria um novo produto com os seguintes atributos: descrição, valor de venda, código de barras, seção, estoque inicial, data de validade (opcional) e imagens.",
    response_model=ProductRead
)
def create_product_endpoint(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    return create_product(db, product)

@router.get(
    "/{product_id}",
    summary="Obter produto por ID",
    description="Retorna os detalhes de um produto específico com base no seu ID único.", 
    response_model=ProductRead
)
def get_product_by_id(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put(
    "/{product_id}",
    summary="Atualizar produto por ID",
    description="Atualiza os dados de um produto existente. É possível modificar a descrição, valor, estoque, validade e outros campos.",
    response_model=ProductRead
)
def update_product_by_id(
    product_id: int, 
    product: ProductUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    updated = update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated

@router.delete(
    "/{product_id}",
    summary="Excluir produto por ID",
    description="Remove permanentemente um produto do sistema com base em seu ID."
)
def delete_product_by_id(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"msg": "Produto removido com sucesso"}
