import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

from app.data.database import Base


class ProductProviderModel(Base):
    __tablename__ = "product_providers"
    __table_args__ = {"schema": "public"}

    product_id = Column(UUIDType(as_uuid=True), ForeignKey("public.products.id"), primary_key=True)
    provider_id = Column(UUIDType(as_uuid=True), ForeignKey("public.providers.id"), primary_key=True)

    purchase_price = Column(Float, nullable=False,  default=0)
    delivery_time = Column(Integer, nullable=False,  default=0)
    company_id = Column(UUIDType(as_uuid=True), nullable=True)
    created_by = Column(UUIDType(as_uuid=True), nullable=True)
    updated_by = Column(UUIDType(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    product = relationship(
        "ProductModel",
        back_populates="product_providers",
        overlaps="providers"
    )

    provider = relationship(
        "ProviderModel",
        back_populates="product_providers",
        overlaps="products"
    )
