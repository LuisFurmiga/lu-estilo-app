# lu-estilo-app/app/tests/test_auth.py
import pytest

from httpx import AsyncClient, ASGITransport
from app.main import create_app
app = create_app()

@pytest.mark.asyncio
async def test_register_and_login():
    # Testa o registro e login de usuários
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Registro
        res = await ac.post("/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123456"
        })
        assert res.status_code in (200, 400)
        if res.status_code == 200:
            assert res.json()["email"] == "test@example.com"
        else:
            print("Registro falhou:", res.json())

        # Login
        res = await ac.post("/auth/login", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123456"
        })
        assert res.status_code == 200
        assert "access_token" in res.json()