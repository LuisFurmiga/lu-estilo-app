from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

os.environ["PYTEST_ENV"] = "0"  # 1 = Simula o ambiente de teste

# Verifica se está rodando testes
if os.getenv("PYTEST_ENV") == "1":
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env.test"))
else:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





