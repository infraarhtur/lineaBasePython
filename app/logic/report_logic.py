from datetime import date
from typing import List

from sqlalchemy.orm import Session

from app.data.report_repository import ReportRepository
from app.models.reports.report_sales_by_products_model import (
    ReportSalesByProductsModel,
)
from app.models.reports.report_summary_sales_model import (
    SalesSummaryByPaymentModel,
)


class ReportLogic:
    def __init__(self, db: Session):
        self.repo = ReportRepository(db)

    def get_sales_summary(self, start_date: date, end_date: date) -> List[SalesSummaryByPaymentModel]:
        return self.repo.get_sales_summary_by_payment_method(start_date, end_date)
    
    def get_sales_by_products(self, start_date: date, end_date: date, status: str) -> List[ReportSalesByProductsModel]:
        return self.repo.get_sales_by_products(start_date, end_date, status)
