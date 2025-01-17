# app/view/client_endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.data.database import get_db
from app.models.client_model import ClientCreateSchema, ClientSchema
from app.logic.client_logic import ClientLogic

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
    service = ClientLogic(db)
    return service.create_client(name=client.name, email=client.email, phone=client.phone)

@router.get("/clients/", response_model=List[ClientSchema])
def get_all_clients(db: Session = Depends(get_db)):
    """
    Recupera todos los clientes.

    Args:
        db (Session): Sesión de base de datos inyectada automáticamente.

    Returns:
        List[ClientSchema]: Lista de todos los clientes.
    """
    service = ClientLogic(db)
    return service.get_all_clients()

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
    service = ClientLogic(db)
    client = service.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client

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
    updated_client = service.update_client(
        client_id=client_id, name=client.name, email=client.email, phone=client.phone
    )
    if not updated_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return updated_client

@router.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: str, db: Session = Depends(get_db)):
    """
    Elimina un cliente por su ID.

    Args:
        client_id (str): ID del cliente a eliminar.
        db (Session): Sesión de base de datos inyectada automáticamente.

    Raises:
        HTTPException: Si el cliente no existe.
    """
    service = ClientLogic(db)
    success = service.delete_client(client_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
