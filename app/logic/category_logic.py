import json
import uuid
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.category_repository import CategoryRepository
from app.models.category_model import CategoryModel
from app.services.message_service import MessageService
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError


class CategoryLogic:
    """
    Clase que encapsula la lógica de negocio para los categoryes.
    Se comunica con el CategoryRepository para manejar las operaciones de datos.
    """
    def __init__(self, db: Session = None):
        """
        Constructor de la clase ClientLogic.

        Args:
            db (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """

        self.db = db
        if self.db is not None :
            self.category_repo = CategoryRepository(self.db)
    
    def __delete__(self):
        """Cierra la sesión automáticamente cuando se destruye la instancia"""
        if self.db is not None :
            self.db.close()

    def create_category(self, **kwargs) -> CategoryModel:
        """
            Crea un nuevo categoria.

            Args:
                **kwargs: Argumentos con las propiedades del categorye (excepto el ID).

            Returns:
                CategoryModel: Instancia del categorye creado.

            Raises:
                ValidationError: Si los datos proporcionados son inválidos.
                SQLAlchemyError: Si ocurre un error durante la operación en la base de datos.
        """
        try:
            # Validar campos obligatorios
            if not kwargs.get("name"):
                raise ValidationError(const.ERROR_MISSING_REQUIRED_FIELDS)

            # Crear instancia del categorye
            category = CategoryModel(**kwargs)
            return self.category_repo.save(category)
        
        except SQLAlchemyError as e:
            if "UNIQUE constraint failed" in str(e.orig):  
                raise ValidationError(const.ERROR_EMAIL_ALREADY_EXISTS.format(email = kwargs.get('email')))             
            raise e
       

    def get_category_by_id(self, category_id: str) -> Optional[CategoryModel]:
        """
        Recupera un categorye por su ID.

        Args:
            category_id (str): ID del categorye a buscar.

        Returns:
            Optional[CategoryModel]: Cliente encontrado o None si no existe.
        """
        # Convertir a UUID antes de usar en la consulta        

        try:
            # Validar que el category_id sea un UUID válido
            category_id = uuid.UUID(category_id) 
        except ValueError:
            raise ValidationError(const.ERROR_INVALID_UUID)
        

        try:
            category = self.category_repo.fetch(category_id)
        except SQLAlchemyError as e:
            raise e

        if not category:
            raise NotFoundError(const.ERROR_CLIENT_NOT_FOUND.format(category_id=category_id))
        return category
       

    def get_all_category(self) -> List[CategoryModel]:
        """
        Recupera todos los categoryes.

        Returns:
            List[CategoryModel]: Lista de todos los categoryes.
        """

        try:
            categorys = self.category_repo.fetch_all()
        except SQLAlchemyError as e:
            raise e
        return categorys

    def update_category(self, category_id: str, **kwargs) -> Optional[CategoryModel]: 
        """
        Actualiza la información de un categorye.

        Args:
            category_id (str): ID del categorye a actualizar.
            name (Optional[str]): Nuevo nombre del categorye (opcional).
            email (Optional[str]): Nuevo email del categorye (opcional).

        Returns:
            Optional[CategoryModel]: Cliente actualizado o None si no se encontró.
        """
        try:
            category =self.get_category_by_id(category_id)
            
            if category:
                if kwargs.get("name"):
                    category.name = kwargs.get("name")
                if kwargs.get("description"):
                    category.description = kwargs.get("name")
                

                return self.category_repo.save(category)
        except SQLAlchemyError as e:
            if "UNIQUE constraint failed" in str(e.orig):
                raise ValidationError(const.ERROR_EMAIL_ALREADY_EXISTS.format(name = kwargs.get("name")))
            raise e


    def delete_category(self, category_id: str) -> bool:
        """
        Elimina un categorye por su ID.

        Args:
            category_id (str): ID del categorye a eliminar.

        Returns:
            bool: True si el categorye fue eliminado, False si no existe.
        """
        try:
            # Verificar que el categorye exista
            category = self.get_category_by_id(str(category_id))
            category.is_active = False  # Marcar como inactivo en lugar de eliminar físicamente
            # Eliminar categorye
            self.category_repo.save(category)
            return True
        except SQLAlchemyError as e:
            raise e

    def create_category_queue(self, **kwargs):
        """
            Crea un nuevo categorye.

            Args:
                **kwargs: Argumentos con las propiedades del categorye (excepto el ID).

            Returns:
                CategoryModel: Instancia del categorye creado.

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

       