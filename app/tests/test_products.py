# lu-estilo-app/app/tests/test_products.py
import pytest

from datetime import date
from httpx import AsyncClient, ASGITransport
from app.main import create_app
app = create_app()

@pytest.mark.asyncio
async def test_create_and_get_product():
    # Testa a criação e listagem de produtos
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

        res = await ac.post("/products/", json={
            "description": "Produto Teste",
            "price": 19.99,
            "barcode": "123456789",
            "section": "Roupas",
            "stock": 10,
            "image": "https://www.purina.com/.netlify/images?url=https%3A%2F%2Flive.purina.com%2Fsites%2Fdefault%2Ffiles%2Fproducts%2F2024-01%2Fdc_softbites_chkn_72oz_00017800101059_vanity-hero_1000x1000.jpg",
            "expiration_date": date.today().isoformat()
        }, headers=headers)
        assert res.status_code == 200
        assert res.json()["barcode"] == "123456789"

        res = await ac.get("/products/", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
