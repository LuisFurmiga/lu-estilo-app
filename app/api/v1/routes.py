# lu-estilo-app/app/api/v1/routes.py
from fastapi import APIRouter, Depends
from app.api.v1.endpoints import auth, clients, products, orders
from app.api.v1.endpoints.auth import get_current_user

api_router = APIRouter()

# Protege globalmente com JWT
clients.router.dependencies.append(Depends(get_current_user))
products.router.dependencies.append(Depends(get_current_user))
orders.router.dependencies.append(Depends(get_current_user))

# Registro das rotas
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])

