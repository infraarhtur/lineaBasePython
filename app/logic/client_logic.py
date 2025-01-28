# app/logic/client_logic.py
from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.data.client_repository import ClientRepository
from app.models.client_model import ClientModel
from typing import Optional, List
import uuid
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError


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

            Raises:
                ValidationError: Si los datos proporcionados son inválidos.
                SQLAlchemyError: Si ocurre un error durante la operación en la base de datos.
        """
        try:
            # Validar campos obligatorios
            if not kwargs.get("name") or not kwargs.get("email"):
                raise ValidationError(const.ERROR_MISSING_REQUIRED_FIELDS)

            # Crear instancia del cliente
            client = ClientModel(**kwargs)
            return self.client_repo.save(client)
        
        except SQLAlchemyError as e:
            if "UNIQUE constraint failed" in str(e.orig): 
                raise ValidationError(const.ERROR_EMAIL_ALREADY_EXISTS.format(email = kwargs.get('email')))             
            raise e
       

    def get_client_by_id(self, client_id: str) -> Optional[ClientModel]:
        """
        Recupera un cliente por su ID.

        Args:
            client_id (str): ID del cliente a buscar.

        Returns:
            Optional[ClientModel]: Cliente encontrado o None si no existe.
        """
        # Convertir a UUID antes de usar en la consulta        

        try:
            # Validar que el client_id sea un UUID válido
            client_id = uuid.UUID(client_id)
        except ValueError:
            raise ValidationError(const.ERROR_INVALID_UUID)
        

        try:
            client = self.client_repo.fetch(client_id)
        except SQLAlchemyError as e:
            raise e

        if not client:
            raise NotFoundError(const.ERROR_CLIENT_NOT_FOUND.format(client_id=client_id))
        return client
       

    def get_all_clients(self) -> List[ClientModel]:
        """
        Recupera todos los clientes.

        Returns:
            List[ClientModel]: Lista de todos los clientes.
        """

        try:
            clients = self.client_repo.fetch_all()
        except SQLAlchemyError as e:
            raise e
        return clients

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
        try:
            client =self.get_client_by_id(client_id)
            
            if client:
                if name:
                    client.name = name
                if email:
                    client.email = email
                if phone:
                    client.phone = phone
                return self.client_repo.save(client)
        except SQLAlchemyError as e:
            if "UNIQUE constraint failed" in str(e.orig):
                raise ValidationError(const.ERROR_EMAIL_ALREADY_EXISTS.format(email = email))
            raise e


    def delete_client(self, client_id: str) -> bool:
        """
        Elimina un cliente por su ID.

        Args:
            client_id (str): ID del cliente a eliminar.

        Returns:
            bool: True si el cliente fue eliminado, False si no existe.
        """
        try:
            # Verificar que el cliente exista
            client = self.get_client_by_id(str(client_id))
            # Eliminar cliente
            return self.client_repo.delete(client)
        except SQLAlchemyError as e:
            raise e
