import json
import uuid
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.client_repository import ClientRepository
from app.models.client_model import ClientModel
from app.services.message_service import MessageService
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError


class ClientLogic:
    """
    Clase que encapsula la lógica de negocio para los clientes.
    Se comunica con el ClientRepository para manejar las operaciones de datos.
    """
    def __init__(self, db: Session = None):
        """
        Constructor de la clase ClientLogic.

        Args:
            db (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """

        self.db = db
        if self.db is not None :
            self.client_repo = ClientRepository(self.db)
    
    def __delete__(self):
        """Cierra la sesión automáticamente cuando se destruye la instancia"""
        if self.db is not None :
            self.db.close()

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

    def update_client(self, client_id: str, name: str = None, email: str = None, phone: str = None, address: str = None,comment: str = None) -> Optional[ClientModel]: 
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
                if address:
                    client.address = address
                if comment:
                    client.comment =comment
                

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
            client.is_active = False  # Marcar como inactivo en lugar de eliminar físicamente
            # Eliminar cliente
            self.client_repo.save(client)
            return True
        except SQLAlchemyError as e:
            raise e

    def create_client_queue(self, **kwargs):
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
            
            message_service = MessageService()
        # Procesar mensajes recibidos en la cola
            # message_service.process_messages()            
            return message_service.enviar_mensaje(kwargs)       
        
        except Exception as e:
            raise e
        
    def process_messages_queue(self):
        """
        Recibe y procesa los mensajes de la cola SQS
         """
        try:            
            message_service = MessageService()
            return message_service.process_messages()
        except Exception as e:
            raise e

       