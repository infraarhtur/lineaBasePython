from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.logic.report_logic import ReportLogic
from app.models.reports.report_sales_by_products_model import (
    ReportSalesByProductsModel,
)
from app.models.reports.report_summary_sales_model import (
    SalesSummaryByPaymentModel,
)
from app.utils import constans as const
from app.utils.error_handling import AppError, NotFoundError, ValidationError

router = APIRouter()

@router.get("/report_sale_summary_payment", response_model=List[SalesSummaryByPaymentModel])
def get_report_sale_summary_payment(start_date: date = Query(..., description="Fecha de inicio"),
    end_date: date = Query(..., description="Fecha de fin"),
    db: Session = Depends(get_db)):
    """
    Recupera todos los proveedores.
    """
    logic = ReportLogic(db)
    try:
        return logic.get_sales_summary(start_date, end_date)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.get("/report_sales_by_products", response_model=List[ReportSalesByProductsModel])
def get_report_sales_by_products(start_date: date = Query(..., description="Fecha de inicio"),
    end_date: date = Query(..., description="Fecha de fin"),
    status: str = Query(..., description="Estado de la venta"),
    db: Session = Depends(get_db)):
    """
    Recupera el reporte de ventas por productos.
    """
    logic = ReportLogic(db)
    try:
        return logic.get_sales_by_products(start_date, end_date, status)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    