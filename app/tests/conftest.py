# lu-estilo-app/app/tests/conftest.py
'''
Para executar os testes, use o comando:
psql -U luisfurmiga -d luestilo_test -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
alembic revision --autogenerate -m "create tables"
alembic upgrade head

Linux:
PYTEST_ENV=1 pytest
Windows:
$env:PYTEST_ENV="1"; pytest -s
'''
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from app.db.session import get_db
from app.db.base import Base
from app.main import create_app
app = create_app()

TEST_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)

    # Cria as tabelas diretamente
    Base.metadata.create_all(bind=engine)

    yield

    # Opcionalmente limpar
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
