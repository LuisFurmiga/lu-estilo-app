# lu-estilo-app/app/api/v1/endpoints/orders.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.user import UserRead
from app.schemas.order import OrderCreate, OrderUpdate, OrderRead
from app.services.order_service import get_orders
from app.models.order import Order
from app.models.product import Product
from app.models.order_item import OrderItem
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
    summary="Listar pedidos com filtros",
    description="Retorna uma lista de pedidos com filtros por período, seção, status, ID e cliente.",
    response_model=List[OrderRead]
)
def list_orders(
    skip: int = 0,
    limit: int = 10,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    section: Optional[str] = Query(None),
    order_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    return get_orders(
        db=db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        section=section,
        order_id=order_id,
        status=status,
        client_id=client_id,
    )

@router.post(
    "/",
    summary="Criar Pedido",
    description="Cria um novo pedido. Verifica o estoque dos produtos antes de criar o pedido.",
    response_model=OrderRead
)
def create_order(
    order: OrderCreate, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    # Verificar estoque
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {item.product_id} não encontrado")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {product.description}")
        product.stock -= item.quantity

    # Criar o pedido
    db_order = Order(client_id=order.client_id, status="pendente")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Criar os itens do pedido
    for item in order.items:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.commit()
    db.refresh(db_order)

    return db_order

@router.get(
    "/{order_id}",
    summary="Obter Pedido",
    description="Retorna os detalhes de um pedido específico com base no seu ID único..",
    response_model=OrderRead
)
def get_order(
    order_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.put(
    "/{order_id}",
    summary="Atualizar Pedido",
    description="Atualiza os dados de um pedido existente com base no seu ID único. É possível modificar o status do pedido.",
    response_model=OrderRead
)
def update_order(
    order_id: int, 
    order: OrderUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete(
    "/{order_id}",
    summary="Excluir Pedido",
    description="Remove permanentemente um pedido do sistema com base no seu ID."
)
def delete_order(
    order_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(order)
    db.commit()
    return {"msg": "Pedido removido com sucesso"}