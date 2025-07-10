
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import UUID, Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

from app.data.database import Base


class ProviderModel(Base):
    """
    Modelo de SQLAlchemy que representa la tabla de proveedores.
    """
    __tablename__ = "providers"
    __table_args__ = {"schema": "public"}

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)

    # Relación muchos a muchos con productos
    products = relationship(
        "ProductModel",
        secondary="public.product_providers",
        back_populates="providers",
        overlaps="product,product_providers"
    )

    # Relación directa con la tabla intermedia
    product_providers = relationship(
        "ProductProviderModel",
        back_populates="provider",
        cascade="all, delete-orphan",
        overlaps="products"
    )

    def __repr__(self):
        return f"<ProviderModel(id={self.id}, name={self.name}, is_active={self.is_active}, created_at={self.created_at})>"


# ----------------------------
# Esquemas Pydantic
# ----------------------------

class ProviderCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del proveedor")
    phone: Optional[str] = Field(None, description="Número de teléfono")
    email: Optional[str] = Field(None, description="Correo electrónico")
    address: Optional[str] = Field(None, description="Dirección del proveedor")
    is_active: bool = Field(True, description="Indica si el proveedor está activo")
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Fecha y hora de creación del proveedor"
    )


class ProviderSchema(ProviderCreateSchema):
    id: uuid.UUID = Field(..., description="Identificador único del proveedor")

    class Config:
        from_attributes = True
