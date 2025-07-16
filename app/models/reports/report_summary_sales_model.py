from pydantic import BaseModel
from typing import Optional


class SalesSummaryByPaymentModel(BaseModel):
    payment_method_label: str
    total_sales: int
    total_amount: float
    total_discount: float