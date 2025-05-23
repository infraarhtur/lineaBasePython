from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.logic.sale_logic import SaleLogic
from app.models.sale_model import (
    SaleCreateSchema,
    SaleSchema,
    SaleUpdateSchema,
)
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError

# from app.workers.scheduler import start_work

router = APIRouter()

@router.get("/", response_model=List[SaleSchema])
def get_all_sales(db: Session = Depends(get_db)):

    """
    Recupera todas las ventas.

    Args:
        db (Session): Sesión activa de SQLAlchemy para la base de datos.

    Returns:
        List[ProductSchema]: Lista de todos los productos.

    Raises:
        HTTPException: Si ocurre un error relacionado con la base de datos.
    """
    logic = SaleLogic(db)
    try:
        sales = logic.get_all_sales()
        return sales
    except Exception as e:
        # Captura de errores inesperados o de la base de datos
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.get("/{sale_id}", response_model=SaleSchema)
def get_sale_by_id(sale_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene una venta específica por ID.
    """
    logic = SaleLogic(db)
    try:
        sale = logic.get_sale_by_id(sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        return sale 
    except Exception as e:
            # Captura de errores inesperados o de la base de datos
            raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.post("/", response_model=SaleSchema, status_code=status.HTTP_201_CREATED)
def create_sale(sale_data: SaleCreateSchema, db: Session = Depends(get_db)):
    """
    Crea una nueva venta con sus detalles.
    """
    try:
        sale_logic = SaleLogic(db)
        new_sale = sale_logic.create_sale(sale_data)
        return new_sale        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{sale_id}", response_model=SaleSchema)
def update_sale(sale_id: UUID, sale_data: SaleUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza una venta existente.
    """
    logic = SaleLogic(db)
    updated_sale = logic.update_sale(sale_id, sale_data)
    if not updated_sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return updated_sale
