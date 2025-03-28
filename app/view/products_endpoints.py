# app/view/product_endpoints.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.logic.product_logic import ProductLogic
from app.models.products_model import ProductCreateSchema, ProductSchema, ProductStockUpdateSchema
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError
from app.workers.scheduler import start_worker

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):

    """
    Recupera todos los productos.

    Args:
        db (Session): Sesión activa de SQLAlchemy para la base de datos.

    Returns:
        List[ProductSchema]: Lista de todos los productos.

    Raises:
        HTTPException: Si ocurre un error relacionado con la base de datos.
    """
    logic = ProductLogic(db)
    try:
        products = logic.get_all_products()
        return products
    except Exception as e:
        # Captura de errores inesperados o de la base de datos
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    


@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """
    Recupera un producto por su ID.

    Args:
        product_id (str): ID del Producto a buscar.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ProductSchema: producto encontrado.

    Raises:
        HTTPException: Si el producto no existe.
    """

    logic = ProductLogic(db)
    try:
        product = logic.get_product_by_id(product_id)
        return product
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    
@router.delete("/{product_id}" ,response_model=bool,
                status_code=status.HTTP_200_OK)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    """
    Elimina un producte por su ID.

    Args:
        product_id (str): ID del producto a eliminar.
        db (Session): Sesión activa de SQLAlchemy para la base de datos.

    Raises:
        HTTPException: Si ocurre algún error relacionado con validaciones,
          datos no encontrados o errores internos.
    """
    logic = ProductLogic(db)
    try:
        return logic.delete_product(product_id)
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    
    
@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto.

    Args:
        product (ProductCreateSchema): Datos del producto a crear.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ProductSchema: Producto creado.
    """
    try:
        service = ProductLogic(db)       
        return service.create_product(**product.model_dump())
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    
@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: str, product: ProductCreateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un producte.

    Args:
        product_id (str): ID del producte a actualizar.
        product (ProductCreateSchema): Datos actualizados del producte.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ProductSchema: Producte actualizado.

    Raises:
        HTTPException: Si el producte no existe.
    """
    service = ProductLogic(db)
    try:
        updated_product = service.update_product(product_id,
           **product.model_dump()
        )        
        return updated_product
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    
@router.patch("/{product_id}/stock", response_model=ProductSchema)
def update_product_stock(product_id: str, payload: ProductStockUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza únicamente el stock de un producto.

    Args:
        product_id (str): ID del producto.
        payload (ProductStockUpdateSchema): Nuevo valor del stock.
        db (Session): Sesión activa de SQLAlchemy.

    Returns:
        ProductSchema: Producto con el stock actualizado.

    Raises:
        HTTPException: Si hay errores de validación o no se encuentra el producto.
    """
    service = ProductLogic(db)
    try:
        updated_product = service.update_product_stock(product_id, payload.stock)
        return updated_product
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

