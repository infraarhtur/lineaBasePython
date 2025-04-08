import uuid
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as UUIDType

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

    def __repr__(self):
        return f"<ProviderModel(id={self.id}, name={self.name})>"


# ----------------------------
# Esquemas Pydantic
# ----------------------------

class ProviderCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del proveedor")
    phone: Optional[str] = Field(None, description="Número de teléfono")
    email: Optional[str] = Field(None, description="Correo electrónico")
    address: Optional[str] = Field(None, description="Dirección del proveedor")


class ProviderSchema(ProviderCreateSchema):
    id: uuid.UUID = Field(..., description="Identificador único del proveedor")

    class Config:
        from_attributes = True
