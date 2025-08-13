import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

from app.data.database import Base
from app.models.client_model import ClientSchema


class SaleModel(Base):
    """
    Modelo de SQLAlchemy que representa la tabla de ventas (sales).
    """
    __tablename__ = "sales"
    __table_args__ = {"schema": "public"}

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    client_id = Column(UUIDType(as_uuid=True), ForeignKey("public.clients.id", ondelete="SET NULL"), nullable=True)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    total_discount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="pending", nullable=False)
    payment_method = Column(String, nullable=True)
    comment = Column(Text, nullable=True)
    created_by = Column(UUIDType(as_uuid=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    company_id = Column(UUIDType(as_uuid=True), nullable=True)
    updated_by = Column(UUIDType(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # Relación con detalles (usamos string para evitar errores de inicialización)
    details = relationship(
        "SaleDetailModel",
        back_populates="sale",
        cascade="all, delete-orphan"
    )
    client = relationship("ClientModel", back_populates="sales")

    def __repr__(self):
        return (
            f"<SaleModel(id={self.id}, client_id={self.client_id}, sale_date={self.sale_date}, "
            f"total_amount={self.total_amount}, status={self.status}, payment_method={self.payment_method},"
            f"total_discount={self.total_discount}>"
        )
# -------------------------------
# Esquemas Pydantic (para FastAPI)
# -------------------------------
# 🔹 Detalle de venta (entrada)
class SaleDetailCreateSchema(BaseModel):
    product_id: uuid.UUID = Field(..., description="ID del producto")
    quantity: int = Field(..., gt=0, description="Cantidad vendida")
    discount: float = Field(default=0.00, ge=0.0, description="Descuento aplicado")
    tax: float = Field(default=0.00, ge=0.0, description="Impuesto aplicado")
    subtotal: float = Field(..., gt=0, description="Subtotal del producto (sin descuento ni impuestos)")
    total: Optional[float] = Field(None, description="Total con descuento e impuestos")
    unit_cost: Optional[float] = Field(None, description="Costo del producto al momento de la venta")
    comment: Optional[str] = Field(None, description="Comentario adicional sobre el ítem vendido")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la compañía")
    created_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que creó el detalle")
    updated_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que actualizó el detalle")

# 🔹 Detalle de venta (respuesta)
class SaleDetailSchema(SaleDetailCreateSchema):
    id: uuid.UUID = Field(..., description="ID del detalle de venta")
    product_name: Optional[str] = Field(None, description="Nombre del producto")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la compañía")
    created_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que creó el detalle")
    updated_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que actualizó el detalle")

    class Config:
        from_attributes = True


# 🔸 Venta (entrada)
class SaleCreateSchema(BaseModel):
    client_id: uuid.UUID = Field(..., description="ID del cliente")
    sale_date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Fecha de la venta")
    total_amount: float = Field(..., gt=0, description="Total de la venta")
    total_discount: float = Field(..., ge=0, description="Total del descuento aplicado")
    status: Optional[str] = Field(default="pending", description="Estado de la venta (pending, paid, canceled)")
    payment_method: Optional[str] = Field(None, description="Método de pago (tarjeta, efectivo, etc.)")
    comment: Optional[str] = Field(None, description="Comentario adicional sobre la venta")
    created_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que creó la venta")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la compañía")
    updated_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que actualizó la venta")
    #cliente
    client: Optional[ClientSchema] = Field(..., description="Detalles del cliente")
    # Lista de productos vendidos
    details: List[SaleDetailCreateSchema] = Field(..., description="Lista de productos vendidos en la venta")

class SaleUpdateSchema(BaseModel):
    client_id: Optional[uuid.UUID] = Field(None, description="ID del cliente")
    sale_date: Optional[datetime] = Field(None, description="Fecha de la venta")
    total_amount: Optional[float] = Field(None, gt=0, description="Total de la venta")
    total_discount: Optional[float] = Field(None, ge=0, description="Total del descuento aplicado")
    status: Optional[str] = Field(None, description="Estado (pending, paid, canceled)")
    payment_method: Optional[str] = Field(None, description="Método de pago")
    comment: Optional[str] = Field(None, description="Comentario")
    created_by: Optional[uuid.UUID] = Field(None, description="ID del creador")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la compañía")
    updated_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que actualizó la venta")

    class Config:
        from_attributes = True

# 🔸 Venta (respuesta)
class SaleSchema(SaleCreateSchema):
    id: uuid.UUID = Field(..., description="ID de la venta")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la compañía")
    created_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que creó la venta")
    updated_by: Optional[uuid.UUID] = Field(None, description="ID del usuario que actualizó la venta")
    details: List[SaleDetailSchema] = Field(..., description="Detalles de la venta")
    client: Optional[ClientSchema] = Field(..., description="Detalles del cliente")
    class Config:
        from_attributes = True

