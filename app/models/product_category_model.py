import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.data.database import Base


class ProductCategoryModel(Base):
    __tablename__ = "product_categories"
    __table_args__ = {"schema": "public"}

    product_id = Column(ForeignKey("public.products.id"), primary_key=True)
    category_id = Column(ForeignKey("public.categories.id"), primary_key=True)
    company_id = Column(UUID(as_uuid=True), nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, nullable=True)
