from sqlalchemy import Column, ForeignKey

from app.data.database import Base


class ProductCategoryModel(Base):
    __tablename__ = "product_categories"
    __table_args__ = {"schema": "public"}

    product_id = Column(ForeignKey("public.products.id"), primary_key=True)
    category_id = Column(ForeignKey("public.categories.id"), primary_key=True)
