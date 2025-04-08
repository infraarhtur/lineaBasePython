import uuid
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, String
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

    #Relación con productos (muchos a muchos)
    products = relationship(
        "ProductModel",
        secondary="public.product_categories",
        back_populates="categories"
    )

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name}, description={self.description})>"


class CategoryCreateSchema(BaseModel):
    """
    Esquema para la creación de una categoría.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría")
    description: Optional[str] = Field(None, description="Descripción de la categoría")


class CategorySchema(CategoryCreateSchema):
    """
    Esquema para representar una categoría con un ID.
    """
    id: uuid.UUID = Field(..., description="Identificador único de la categoría")

    class Config:
        from_attributes = True  # Permite la compatibilidad con modelos ORM
