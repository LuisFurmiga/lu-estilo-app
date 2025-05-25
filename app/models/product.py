# lu-estilo-app/app/models/product.py
from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    barcode = Column(String, unique=True, index=True)
    section = Column(String, index=True)
    stock = Column(Integer, default=0)
    expiration_date = Column(Date, nullable=True)
    image = Column(String, nullable=True)
    available = Column(Boolean, default=True)