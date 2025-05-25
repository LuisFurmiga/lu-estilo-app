# lu-estilo-app/app/api/v1/endpoints/clients.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.user import UserRead
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.services.client_service import *
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
    summary="Listar clientes",
    description="Retorna uma lista de todos os clientes cadastrados no sistema, com suporte a filtros e paginação.",
    response_model=List[ClientRead]
)
def list_clients(
    skip: int = 0, 
    limit: int = 10, 
    name: str = None, 
    email: str = None, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    return get_clients(db, skip, limit, name, email)

@router.post(
    "/", 
    summary="Criar novo cliente",
    description="Cria um novo cliente com nome, email e CPF. O CPF é validado antes da inserção.",
    response_model=ClientRead
)
def create_new_client(
    client: ClientCreate, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    return create_client(db, client)

@router.get(
    "/{client_id}", 
    summary="Obter cliente por ID",
    description="Retorna os dados completos de um cliente específico, identificado pelo seu ID único.",
    response_model=ClientRead
)
def get_client_by_id(
    client_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_client

@router.put(
    "/{client_id}",
    summary="Atualizar cliente por ID",
    description="Atualiza as informações de um cliente existente, com base no ID fornecido. Os dados antigos são substituídos pelos novos.",
    response_model=ClientRead
)
def update_client_by_id(
    client_id: int, 
    client: ClientUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    updated = update_client(db, client_id, client)
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return updated

@router.delete(
    "/{client_id}",
    summary="Excluir cliente por ID",
    description="Remove um cliente permanentemente do banco de dados, a partir do seu ID."
)
def delete_client_by_id(
    client_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserRead = Depends(get_current_user)
    ):
    deleted = delete_client(db, client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"msg": "Cliente removido com sucesso"}
