import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.data.database import Base


class CategoryModel(Base):
    """
    Modelo de SQLAlchemy que representa la tabla de categorías en la base de datos.
    """
    __tablename__ = "categories"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    company_id = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)

    #Relación con productos (muchos a muchos)
    products = relationship(
        "ProductModel",
        secondary="public.product_categories",
        back_populates="categories"
    )

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name}, description={self.description}, is_active={self.is_active}, created_at={self.created_at})>"


class CategoryCreateSchema(BaseModel):
    """
    Esquema para la creación de una categoría.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría")
    description: Optional[str] = Field(None, description="Descripción de la categoría")
    is_active: bool = Field(True, description="Indicates if the category is active")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la compañía")
    created_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que creó la categoría")
    updated_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que actualizó la categoría")
    created_at: datetime | None = Field(
        default_factory=datetime.utcnow, 
        description="Timestamp when the category was created"
    )

class CategorySchema(CategoryCreateSchema):
    """
    Esquema para representar una categoría con un ID.
    """
    id: uuid.UUID = Field(..., description="Identificador único de la categoría")

    class Config:
        from_attributes = True  # Permite la compatibilidad con modelos ORM
