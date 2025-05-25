# lu-estilo-app/app/tests/test_clients.py
import pytest

from httpx import AsyncClient, ASGITransport
import os
from app.main import create_app
app = create_app()

@pytest.mark.asyncio
async def test_create_and_get_client():
    # Testa a criação e listagem de clientes
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Autenticar
        login = await ac.post("/auth/login", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123456"
        })
        assert login.status_code == 200, f"Login falhou: {login.status_code}, {login.text}"
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Criar cliente
        res = await ac.post("/clients/", json={
            "name": "Cliente Teste",
            "email": "cliente@example.com",
            "cpf": os.getenv("CPF_1")
        }, headers=headers)
        assert res.status_code == 200
        assert res.json()["cpf"] == os.getenv("CPF_1")

        # Listar clientes
        res = await ac.get("/clients/", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
