# app/view/provider_endpoints.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.logic.provider_logic import ProviderLogic
from app.models.provider_model import ProviderCreateSchema, ProviderSchema
from app.utils import constans as const
from app.utils.error_handling import AppError, NotFoundError, ValidationError

router = APIRouter()


@router.post("/", response_model=ProviderSchema, status_code=status.HTTP_201_CREATED)
def create_provider(provider: ProviderCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo proveedor.
    """
    logic = ProviderLogic(db)
    try:
        return logic.create_provider(**provider.model_dump())
    except AppError as ae:
        raise HTTPException(status_code=ae.status_code, detail=str(ae))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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


@router.get("/{provider_id}", response_model=ProviderSchema)
def get_provider(provider_id: str, db: Session = Depends(get_db)):
    """
    Recupera un proveedor por su ID.
    """
    logic = ProviderLogic(db)
    try:
        return logic.get_provider_by_id(provider_id)
    except AppError as ae:
        raise HTTPException(status_code=ae.status_code, detail=str(ae))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/{provider_id}", response_model=ProviderSchema)
def update_provider(provider_id: str, provider: ProviderCreateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un proveedor.
    """
    logic = ProviderLogic(db)
    try:
        return logic.update_provider(provider_id, **provider.model_dump())
    except AppError as ae:
        raise HTTPException(status_code=ae.status_code, detail=str(ae))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{provider_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_provider(provider_id: str, db: Session = Depends(get_db)):
    """
    Elimina un proveedor por su ID.
    """
    logic = ProviderLogic(db)
    try:
        return logic.delete_provider(provider_id)
    except AppError as ae:
        raise HTTPException(status_code=ae.status_code, detail=str(ae))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
