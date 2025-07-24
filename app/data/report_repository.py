import uuid
from datetime import date
from typing import List

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.reports.report_sales_by_products_model import (
    ReportSalesByProductsModel,
)
from app.models.reports.report_summary_sales_model import (
    SalesSummaryByPaymentModel,
)


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_sales_summary_by_payment_method(self, start_date: date, end_date: date) -> List[SalesSummaryByPaymentModel]:
        try:
            query = text("""
                SELECT * FROM public.get_sales_summary_by_payment_method(:start_date, :end_date)
            """)
            result = self.db.execute(query, {"start_date": start_date, "end_date": end_date})
            rows = result.fetchall()

            return [
                SalesSummaryByPaymentModel(
                    payment_method_label=row[0],
                    total_sales=row[1],
                    total_amount=row[2],
                    total_discount=row[3]
                )
                for row in rows
            ]
        except SQLAlchemyError as e:
            print("❌ Error al ejecutar el resumen de ventas:", e)
            raise e

    def get_sales_by_products(self, start_date: date, end_date: date, status: str) -> List[ReportSalesByProductsModel]:
        try:
            query = text("""
                SELECT * FROM public.get_sales_by_products(:start_date, :end_date, :status)
            """)
            result = self.db.execute(query, {"start_date": start_date, "end_date": end_date, "status": status  })
            rows = result.fetchall()

            return [
                ReportSalesByProductsModel(
                    product_name=row[0],
                    purchase_price=row[1],
                    sale_price=row[2],
                    total_units_sold=row[3],
                    total_revenue=row[4],
                    total_discount=row[5]
                )
                for row in rows
            ]
        except SQLAlchemyError as e:
            print("❌ Error al ejecutar el reporte de ventas por productos:", e)
            raise e