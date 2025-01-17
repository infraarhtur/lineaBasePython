# app/data/client_repository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.client_model import ClientModel
from typing import Optional, List
import uuid

class ClientRepository:
    """
    Clase que define las operaciones de repositorio para el modelo ClientModel.
    Se encarga de manejar la lógica de acceso a datos mediante SQLAlchemy.
    """
    def __init__(self, db: Session):
        """
        Constructor de la clase ClientRepository.
        
        Args:
            db (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db

    def save(self, client: ClientModel) -> ClientModel:       
        """
        Guarda un cliente en la base de datos.
        
        Args:
            client (ClientModel): Instancia del cliente a guardar.
        
        Returns:
            ClientModel: Instancia del cliente guardado con su ID actualizado.
        
        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación.
        """
        try:
            self.db.add(client)
            self.db.commit()
            self.db.refresh(client)
            return client
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def fetch(self, client_id: str) -> Optional[ClientModel]:
        """
        Recupera un cliente de la base de datos por su ID.
        
        Args:
            client_id (str): ID del cliente a buscar.
        
        Returns:
            Optional[ClientModel]: Cliente encontrado o None si no existe.
        
        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación.
        """
        try:
            # Convertir a UUID antes de usar en la consulta
            client_id = uuid.UUID(client_id)
            return self.db.query(ClientModel).filter(ClientModel.id == client_id).first()
        except SQLAlchemyError as e:
            raise e

    def fetch_all(self) -> List[ClientModel]:
        """
        Recupera todos los clientes de la base de datos.
        
        Returns:
            List[ClientModel]: Lista de todos los clientes.
        
        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación.
        """

        try:
            return self.db.query(ClientModel).all()
        except SQLAlchemyError as e:
            raise e

    def delete(self, client_id: str) -> bool:
        """
        Elimina un cliente de la base de datos por su ID.
        
        Args:
            client_id (str): ID del cliente a eliminar.
        
        Returns:
            bool: True si el cliente fue eliminado, False si no existe.
        
        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación.
        """
        try:
            client = self.fetch(client_id)
            if client:
                self.db.delete(client)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
