from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.logic.provider_logic import ProviderLogic
from app.models.provider_model import ProviderCreateSchema, ProviderSchema
from app.utils import constans as const
from app.utils.error_handling import AppError, NotFoundError, ValidationError

router = APIRouter()

@router.get("/", response_model=List[ProviderSchema])
def get_all_providers(db: Session = Depends(get_db)):
    """
    Recupera todos los proveedores.
    """
    logic = ProviderLogic(db)
    try:
        return logic.get_all_providers()
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")