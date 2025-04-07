# app/view/category_endpoints.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.logic.category_logic import CategoryLogic
from app.models.category_model import CategoryCreateSchema, CategorySchema
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError
from app.workers.scheduler import start_worker

router = APIRouter()

@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreateSchema, db: Session = Depends(get_db)):
    """
    Crea una nueva categoria.

    Args:
        category (CategoryCreateSchema): Datos del categoria a crear.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        CategoryCreateSchema: Cliente creado.
    """
    try:
        service = CategoryLogic(db)
        # return service.create_category(name=category.name, email=category.email, phone=category.phone,address=category.address,comment=category.comment)
        return service.create_category(**category.model_dump())
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

    

@router.get("/", response_model=List[CategorySchema])
def get_all_category(db: Session = Depends(get_db)):

    """
    Recupera todos los categorias.

    Args:
        db (Session): Sesión activa de SQLAlchemy para la base de datos.

    Returns:
        List[CategoryCreateSchema]: Lista de todos los categorias.

    Raises:
        HTTPException: Si ocurre un error relacionado con la base de datos.
    """
    logic = CategoryLogic(db)
    try:
        category = logic.get_all_category() 
        return category
    except Exception as e:
        # Captura de errores inesperados o de la base de datos
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: str, db: Session = Depends(get_db)):
    """
    Recupera un categoria por su ID.

    Args:
        category_id (str): ID del categoria a buscar.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        CategoryCreateSchema: Cliente encontrado.

    Raises:
        HTTPException: Si el categoria no existe.
    """

    logic = CategoryLogic(db)
    try:
        category = logic.get_category_by_id(category_id)
        return category
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.put("/{category_id}", response_model=CategorySchema)
def update_category(category_id: str, category: CategoryCreateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un categoria.

    Args:
        category_id (str): ID del categoria a actualizar.
        category (CategoryCreateSchema): Datos actualizados del categoria.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        CategoryCreateSchema: Cliente actualizado.

    Raises:
        HTTPException: Si el categoria no existe.
    """
    service = CategoryLogic(db)
    try:
        updated_category = service.update_category(
            category_id=category_id, **category.model_dump()
        )        
        return updated_category
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.delete("/{category_id}" ,response_model=bool,
                status_code=status.HTTP_200_OK)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    """
    Elimina un categoria por su ID.

    Args:
        category_id (str): ID del categoria a eliminar.
        db (Session): Sesión activa de SQLAlchemy para la base de datos.

    Raises:
        HTTPException: Si ocurre algún error relacionado con validaciones,
          datos no encontrados o errores internos.
    """
    logic = CategoryLogic(db)
    try:
        return logic.delete_category(category_id)
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    

@router.post("/category_queue/", response_model=str, 
                 status_code=status.HTTP_202_ACCEPTED)
def create_clien_queue(category: CategoryCreateSchema):
    """
    Crea un nuevo categoria.

    Args:
        category (CategoryCreateSchema): Datos del categoria a crear.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        CategoryCreateSchema: Cliente creado.
    """
    try:
        service = CategoryLogic()
        return service.create_category_queue(name=category.name, email=category.email, phone=category.phone)
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    
    
@router.get("/process_messages_queue/", response_model=List, 
                 status_code=status.HTTP_202_ACCEPTED)
def process_messages_queue():
    """
    Crea un nuevo categoria.

    Args:
        category (CategoryCreateSchema): Datos del categoria a crear.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        CategoryCreateSchema: Cliente creado.
    """
    try:
        service = CategoryLogic()
        return service.process_messages_queue()
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
