import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

from app.data.database import Base


class ProductModel(Base):
    """
    Modelo de SQLAlchemy que representa la tabla de productos.
    """
    __tablename__ = "products"
    __table_args__ = {"schema": "public"}

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    sale_price = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación con categorías (muchos a muchos)
    categories = relationship(
        "CategoryModel",
        secondary="public.product_categories",
        back_populates="products"
    )

    # Relación con proveedores (muchos a muchos directa)
    providers = relationship(
        "ProviderModel",
        secondary="public.product_providers",
        back_populates="products",
        overlaps="product_providers,provider"
    )

    # Relación con la tabla intermedia (acceso a campos como precio de compra)
    product_providers = relationship(
        "ProductProviderModel",
        back_populates="product",
        cascade="all, delete-orphan",
        overlaps="providers,provider"
    )

    def __repr__(self):
        return (
            f"<ProductModel(id={self.id}, name={self.name}, description={self.description}, "
            f"sale_price={self.sale_price}, stock={self.stock}, created_at={self.created_at})>"
        )


# -------------------------------
# Esquemas Pydantic (para FastAPI)
# -------------------------------

class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del producto")
    description: str = Field(..., description="Descripción del producto")
    sale_price: float = Field(..., description="Precio de venta")
    purchase_price: float = Field(..., description="Precio de compra")
    stock: Optional[int] = Field(None, description="Cantidad en inventario")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    category_ids: Optional[List[uuid.UUID]] = Field(default_factory=list, description="IDs de categorías asociadas")
    providers_ids: Optional[List[uuid.UUID]] = Field(default_factory=list, description="IDs de proveedores asociadas")

class CategorySchema(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class ProviderSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    sale_price: float
    purchase_price: float
    stock: Optional[int]
    created_at: Optional[datetime]
    categories: Optional[List[CategorySchema]] = []
    providers: Optional[List[ProviderSchema]] = []

    class Config:
        from_attributes = True


class ProductStockUpdateSchema(BaseModel):
    stock: int = Field(..., description="Cantidad actualizada en inventario")