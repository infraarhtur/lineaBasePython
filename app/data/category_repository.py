import uuid
from typing import List, Optional, cast

import psycopg2
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.category_model import CategoryModel


class CategoryRepository:
    """
    Clase que define las operaciones de repositorio para el modelo CategoryModel.
    Se encarga de manejar la lógica de acceso a datos mediante SQLAlchemy.
    """
    def __init__(self, db: Session):
        """
        Constructor de la clase ClientRepository.
        
        Args:
            db (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db



    def save(self, client: CategoryModel) -> CategoryModel:
        """
        Guarda un cliente en la base de datos.

        Args:
            client (CategoryModel): Instancia del cliente a guardar.

        Returns:
            CategoryModel: Instancia del cliente guardado con su ID actualizado.

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

        

    def fetch(self, client_id: str) -> CategoryModel:
        """
        Recupera un cliente de la base de datos por su ID.
        
        Args:
            client_id (uuid.UUID): ID del cliente a buscar.
        
        Returns:
            CategoryModel: Cliente encontrado o None si no existe.
        """
        try:       
            # Si la sesión está en estado inválido, reiniciarla
            # if self.db.in_transaction():
            #     self.db.rollback()

            query = self.db.query(CategoryModel).filter(CategoryModel.id == client_id)
            print(query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
           
            client = query.first()            

            return client
        except psycopg2.errors.InFailedSqlTransaction:
            print("⚠️ Transacción fallida detectada. Reiniciando sesión de base de datos...")
            self.db.rollback()
            client = self.db.query(CategoryModel).filter(CategoryModel.id == client_id).first()
            return client
        except SQLAlchemyError as e:
            if self.db.in_transaction():
                self.db.rollback()
            print(f"❌ Error SQLAlchemy al recuperar cliente con ID {client_id}: {e}")
            raise e

    def fetch_all(self) -> List[CategoryModel]:
        """
        Recupera todos los clientes de la base de datos.
        
        Returns:
            List[CategoryModel]: Lista de todos los clientes.
        
        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación.
        """

        try:
            return self.db.query(CategoryModel).all()
        except SQLAlchemyError as e:
            raise e

    def delete(self, client: CategoryModel) -> bool:
        """
        Elimina un cliente de la base de datos por su ID.

        Args:
            client_id (str): ID del cliente a eliminar.

        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación en la base de datos.
        """
        try:
            if not client:
                raise ValueError(f"Cliente con ID {client.id} no encontrado.")

            # Eliminar el cliente
            self.db.delete(client)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()  # Revertir la transacción si ocurre un error
            raise e