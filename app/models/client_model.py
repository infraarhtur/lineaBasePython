# app/models/client_model.py
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.data.database import Base


class ClientModel(Base):
    """
    Modelo de SQLAlchemy que representa la tabla de clientes en la base de datos.
    """
    __tablename__ = "clients"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)  # ✅ Campo opcional
    comment = Column(String, nullable=True) # ✅ Campo opcional
    is_active = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)

    sales = relationship("SaleModel", back_populates="client")
    def __repr__(self):
        """
        Representación legible del modelo.
        """
        return f"<ClientModel(id={self.id}, name={self.name}, email={self.email}, phone={self.phone},address={self.address}, comment={self.comment}, is_active={self.is_active}, created_at={self.created_at})>"


class ClientCreateSchema(BaseModel):
    """
    Esquema para la creación de un cliente.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Name of the client")
    email: EmailStr = Field(..., description="Email address of the client")
    phone: str = Field(
        ..., 
        pattern=r"^\+?[1-9]\d{1,14}$", 
        description="Phone number of the client"
    ),
    address: str | None = Field(None, description="Address of the client")  # Campo opcional
    comment: str | None = Field(None, description="Comment about the client")  # Campo opcional
    is_active: bool = Field(True, description="Indicates if the client is active")
    created_at: datetime | None = Field(
        default_factory=datetime.utcnow, 
        description="Timestamp when the client was created"
    )


class ClientSchema(ClientCreateSchema):
    """
    Esquema para representar un cliente con un ID.
    """
    id:  uuid.UUID = Field(..., description="Unique identifier for the client")

    class Config:
        from_attributes = True  # Permite la compatibilidad con modelos ORM
