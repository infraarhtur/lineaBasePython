# app/view/client_endpoints.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.logic.client_logic import ClientLogic
from app.models.client_model import ClientCreateSchema, ClientSchema
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError
from app.workers.scheduler import start_worker

router = APIRouter()

@router.post("/clients/", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo cliente.

    Args:
        client (ClientCreateSchema): Datos del cliente a crear.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ClientSchema: Cliente creado.
    """
    try:
        service = ClientLogic(db)
        return service.create_client(name=client.name, email=client.email, phone=client.phone)
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

    

@router.get("/clients/", response_model=List[ClientSchema])
def get_all_clients(db: Session = Depends(get_db)):

    """
    Recupera todos los clientes.

    Args:
        db (Session): Sesión activa de SQLAlchemy para la base de datos.

    Returns:
        List[ClientSchema]: Lista de todos los clientes.

    Raises:
        HTTPException: Si ocurre un error relacionado con la base de datos.
    """
    logic = ClientLogic(db)
    try:
        clients = logic.get_all_clients()
        return clients
    except Exception as e:
        # Captura de errores inesperados o de la base de datos
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.get("/clients/{client_id}", response_model=ClientSchema)
def get_client(client_id: str, db: Session = Depends(get_db)):
    """
    Recupera un cliente por su ID.

    Args:
        client_id (str): ID del cliente a buscar.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ClientSchema: Cliente encontrado.

    Raises:
        HTTPException: Si el cliente no existe.
    """

    logic = ClientLogic(db)
    try:
        client = logic.get_client_by_id(client_id)
        return client
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.put("/clients/{client_id}", response_model=ClientSchema)
def update_client(client_id: str, client: ClientCreateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un cliente.

    Args:
        client_id (str): ID del cliente a actualizar.
        client (ClientCreateSchema): Datos actualizados del cliente.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ClientSchema: Cliente actualizado.

    Raises:
        HTTPException: Si el cliente no existe.
    """
    service = ClientLogic(db)
    try:
        updated_client = service.update_client(
            client_id=client_id, name=client.name, email=client.email, 
            phone=client.phone
        )        
        return updated_client
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)

@router.delete("/clients/{client_id}" ,response_model=bool,
                status_code=status.HTTP_200_OK)
def delete_client(client_id: str, db: Session = Depends(get_db)):
    """
    Elimina un cliente por su ID.

    Args:
        client_id (str): ID del cliente a eliminar.
        db (Session): Sesión activa de SQLAlchemy para la base de datos.

    Raises:
        HTTPException: Si ocurre algún error relacionado con validaciones,
          datos no encontrados o errores internos.
    """
    logic = ClientLogic(db)
    try:
        return logic.delete_client(client_id)
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
    

@router.post("/clients_queue/", response_model=str, 
                 status_code=status.HTTP_202_ACCEPTED)
def create_clien_queue(client: ClientCreateSchema):
    """
    Crea un nuevo cliente.

    Args:
        client (ClientCreateSchema): Datos del cliente a crear.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ClientSchema: Cliente creado.
    """
    try:
        service = ClientLogic()
        return service.create_client_queue(name=client.name, email=client.email, phone=client.phone)
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
    Crea un nuevo cliente.

    Args:
        client (ClientCreateSchema): Datos del cliente a crear.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        ClientSchema: Cliente creado.
    """
    try:
        service = ClientLogic()
        return service.process_messages_queue()
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=const.ERROR_INTERNAL_SERVER)
