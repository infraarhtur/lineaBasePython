# app/models/product_model.py

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.data.database import Base


class ProductModel(Base):
    """
    Modelo de SQLAlchemy que representa la tabla de productos en la base de datos.
    """
    __tablename__ = "products"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    sale_price = Column(Float, nullable=False)
    purchase_price= Column(Float, nullable=False)
    stock = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return (f"<ProductModel(id={self.id}, name={self.name}, description={self.description}, "
                f"sale_price={self.sale_price}, stock={self.stock}, created_at={self.created_at})>")


class ProductCreateSchema(BaseModel):
    """
    Esquema para la creación de un producto.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Name of the product")
    description: str = Field(..., description="Description of the product")
    sale_price: float = Field(..., description="Sale price of the product")
    purchase_price: float = Field(..., description="purchase price of the product")
    stock: Optional[int] = Field(None, description="Product stock quantity")
    created_at: Optional[datetime] = Field(None, description="Date the product was created")


class ProductSchema(ProductCreateSchema):
    """
    Esquema para representar un producto con un ID.
    """
    id: uuid.UUID = Field(..., description="Unique identifier for the product")

    class Config:
        from_attributes = True  # Permite la compatibilidad con modelos ORM

class ProductStockUpdateSchema(BaseModel):
    stock: int = Field(..., description="Cantidad actualizada en inventario")
