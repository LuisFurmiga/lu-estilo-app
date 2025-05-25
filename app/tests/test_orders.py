# lu-estilo-app/app/tests/test_orders.py
import pytest

from datetime import date
from httpx import AsyncClient, ASGITransport
import os
from app.main import create_app
app = create_app()

@pytest.mark.asyncio
async def test_create_order():
    # Testa a criação e listagem de pedidos
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post("/auth/login", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123456"
        })
        assert login.status_code == 200, f"Login falhou: {login.status_code}, {login.text}"
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Criar cliente para pedido
        client = await ac.post("/clients/", json={
            "name": "Cliente Pedido",
            "email": "cliente2@example.com",
            "cpf": os.getenv("CPF_2")
        }, headers=headers)
        client_id = client.json()["id"]

        # Criar produto
        product = await ac.post("/products/", json={
            "description": "Camisa",
            "price": 50.0,
            "barcode": "123459",
            "section": "Masculina",
            "stock": 5,
            "image": "https://www.purina.com/.netlify/images?url=https%3A%2F%2Flive.purina.com%2Fsites%2Fdefault%2Ffiles%2Fproducts%2F2024-01%2Fdc_softbites_chkn_72oz_00017800101059_vanity-hero_1000x1000.jpg",
            "expiration_date": date.today().isoformat()
        }, headers=headers)
        product_id = product.json()["id"]

        # Criar pedido
        order = await ac.post("/orders/", json={
            "client_id": client_id,
            "items": [{"product_id": product_id, "quantity": 2}]
        }, headers=headers)
        assert order.status_code == 200
        assert order.json()["status"] == "pendente"
