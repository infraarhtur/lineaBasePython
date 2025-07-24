from pydantic import BaseModel, Field
from typing import Optional


class ReportSalesByProductsModel(BaseModel):
    product_name: str = Field(..., description="Nombre del producto")
    purchase_price: float = Field(..., description="Precio de compra")
    sale_price: float = Field(..., description="Precio de venta")
    total_units_sold: int = Field(..., description="Unidades vendidas")
    total_revenue: float = Field(..., description="Ingresos totales")
    total_discount: float = Field(..., description="Descuento total aplicado")
