from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import sentry_sdk
from dotenv import load_dotenv
import os
from app.api.v1.routes import api_router

# Para rodar o servidor, use os comandos:
# alembic revision --autogenerate -m "create tables"
# alembic upgrade head
# uvicorn app.main:app --reload

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

def create_app():
    # Configuração do Sentry
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profile_session_sample_rate to 1.0 to profile 100%
        # of profile sessions.
        profile_session_sample_rate=1.0,
        # Set profile_lifecycle to "trace" to automatically
        # run the profiler on when there is an active transaction
        profile_lifecycle="trace",
    )

    app = FastAPI(
        title="Lu Estilo API",
        version="1.0.0",
        description="Documentação da API de controle de clientes, produtos e pedidos"
    )
    app.include_router(api_router)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Lu Estilo API",
            version="1.0.0",
            description="Documentação personalizada da API",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app

app = create_app()

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

'''
Lista de exemplos de requisições para cada endpoint
user:
{
    "name": "Ameixa",
    "email": "ameixa@email.com",
    "senha": "123456"
}

client:
{
  "name": "Ameixa",
  "email": "ameixa@email.com",
  "cpf": https://www.4devs.com.br/gerador_de_cpf,
  "id": 1
}
{
  "name": "Feia",
  "email": "feia@email.com",
  "cpf": https://www.4devs.com.br/gerador_de_cpf,
  "id": 2
}
{
  "name": "Amora",
  "email": "amora@email.com",
  "cpf": https://www.4devs.com.br/gerador_de_cpf,
  "id": 3
}

Product:
[
  {
    "description": "Dog Chow",
    "price": 19.99,
    "barcode": "7891000244722",
    "section": "Pet Shop",
    "stock": 79,
    "expiration_date": "2025-12-12",
    "image": "https://www.purina.com/.netlify/images?url=https%3A%2F%2Flive.purina.com%2Fsites%2Fdefault%2Ffiles%2Fproducts%2F2024-01%2Fdc_softbites_chkn_72oz_00017800101059_vanity-hero_1000x1000.jpg",
    "available": true,
    "id": 1
  }
]
'''