import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

from app.data.database import Base


class SaleDetailModel(Base):
    """
    Modelo de SQLAlchemy que representa los detalles de una venta.
    """
    __tablename__ = "sale_details"
    __table_args__ = {"schema": "public"}

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    sale_id = Column(UUIDType(as_uuid=True), ForeignKey("public.sales.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUIDType(as_uuid=True), ForeignKey("public.products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    discount = Column(Numeric(10, 2), default=0.00, nullable=False)
    tax = Column(Numeric(10, 2), default=0.00, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=True)
    unit_cost = Column(Numeric(10, 2), nullable=True)
    comment = Column(Text, nullable=True)
    company_id = Column(UUIDType(as_uuid=True), nullable=True)
    created_by = Column(UUIDType(as_uuid=True), nullable=True)
    updated_by = Column(UUIDType(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 🔄 Relación con venta (referencia por nombre para evitar errores de importación circular)
    sale = relationship("SaleModel", back_populates="details")

    # Opcional: relación directa con productos
    product = relationship("ProductModel")

    def __repr__(self):
        return (
            f"<SaleDetailModel(id={self.id}, sale_id={self.sale_id}, product_id={self.product_id}, "
            f"quantity={self.quantity}, subtotal={self.subtotal}, total={self.total}, name={self.product.name if self.product else 'N/A'})>"
        )
