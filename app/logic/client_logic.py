# app/logic/client_logic.py
from sqlalchemy.orm import Session
from app.data.client_repository import ClientRepository
from app.models.client_model import ClientModel
from typing import Optional, List
import uuid


class ClientLogic:
    """
    Clase que encapsula la lógica de negocio para los clientes.
    Se comunica con el ClientRepository para manejar las operaciones de datos.
    """
    def __init__(self, db: Session):
        """
        Constructor de la clase ClientLogic.

        Args:
            db (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.client_repo = ClientRepository(db)

    def create_client(self, **kwargs) -> ClientModel:
        """
        Crea un nuevo cliente.

        Args:
            **kwargs: Argumentos con las propiedades del cliente (excepto el ID).

        Returns:
            ClientModel: Instancia del cliente creado.
        """
        client = ClientModel(**kwargs)
        
        return self.client_repo.save(client)

    def get_client_by_id(self, client_id: str) -> Optional[ClientModel]:
        """
        Recupera un cliente por su ID.

        Args:
            client_id (str): ID del cliente a buscar.

        Returns:
            Optional[ClientModel]: Cliente encontrado o None si no existe.
        """
        return self.client_repo.fetch(client_id)

    def get_all_clients(self) -> List[ClientModel]:
        """
        Recupera todos los clientes.

        Returns:
            List[ClientModel]: Lista de todos los clientes.
        """
        return self.client_repo.fetch_all()

    def update_client(self, client_id: str, name: str = None, email: str = None, phone: str = None) -> Optional[ClientModel]:
        """
        Actualiza la información de un cliente.

        Args:
            client_id (str): ID del cliente a actualizar.
            name (Optional[str]): Nuevo nombre del cliente (opcional).
            email (Optional[str]): Nuevo email del cliente (opcional).

        Returns:
            Optional[ClientModel]: Cliente actualizado o None si no se encontró.
        """
    
        client = self.client_repo.fetch(client_id)
        if client:
            if name:
                client.name = name
            if email:
                client.email = email
            if phone:
                client.phone = phone
            return self.client_repo.save(client)
        return None

    def delete_client(self, client_id: str) -> bool:
        """
        Elimina un cliente por su ID.

        Args:
            client_id (str): ID del cliente a eliminar.

        Returns:
            bool: True si el cliente fue eliminado, False si no existe.
        """
        return self.client_repo.delete(client_id)
