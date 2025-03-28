import json
import uuid
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.product_repository import ProductRepository
from app.models.products_model import ProductModel
from app.services.message_service import MessageService
from app.utils import constans as const
from app.utils.error_handling import NotFoundError, ValidationError


class ProductLogic:
    """
    Clase que encapsula la lógica de negocio para los Productos.
    Se comunica con el productRepository para manejar las operaciones de datos.
    """
    def __init__(self, db: Session = None):
        """
        Constructor de la clase ProductLogic.

        Args:
            db (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """

        self.db = db
        if self.db is not None :
            self.product_repo = ProductRepository(self.db)
    
    def __delete__(self):
        """Cierra la sesión automáticamente cuando se destruye la instancia"""
        if self.db is not None :
            self.db.close()

    def create_product(self, **kwargs) -> ProductModel:
        """
            Crea un nuevo producto.

            Args:
                **kwargs: Argumentos con las propiedades del producto (excepto el ID).

            Returns:
                ProductModel: Instancia del producto creado.

            Raises:
                ValidationError: Si los datos proporcionados son inválidos.
                SQLAlchemyError: Si ocurre un error durante la operación en la base de datos.
        """
        try:
            # Validar campos obligatorios
            if not kwargs.get("name"):
                raise ValidationError(const.ERROR_MISSING_REQUIRED_FIELDS)

            # Crear instancia del producto
            product = ProductModel(**kwargs)
            return self.product_repo.save(product)
        
        except SQLAlchemyError as e:
            if "UNIQUE constraint failed" in str(e.orig):  
                raise ValidationError(const.ERROR_EMAIL_ALREADY_EXISTS.format(email = kwargs.get('email')))             
            raise e
       

    def get_product_by_id(self, product_id: str) -> Optional[ProductModel]:
        """
        Recupera un producto por su ID.

        Args:
            product_id (str): ID del producto a buscar.

        Returns:
            Optional[ProductModel]: producto encontrado o None si no existe.
        """
        # Convertir a UUID antes de usar en la consulta        

        try:
            # Validar que el product_id sea un UUID válido
            product_id = uuid.UUID(product_id) 
        except ValueError:
            raise ValidationError(const.ERROR_INVALID_UUID)
        

        try:
            product = self.product_repo.fetch(product_id)
        except SQLAlchemyError as e:
            raise e

        if not product:
            raise NotFoundError(const.ERROR_PRODUCT_NOT_FOUND.format(product_id=product_id))
        return product
       

    def get_all_products(self) -> List[ProductModel]:
        """
        Recupera todos los productos.

        Returns:
            List[ProductModel]: Lista de todos los productos.
        """

        try:
            products = self.product_repo.fetch_all()
        except SQLAlchemyError as e:
            raise e
        return products

    def update_product(self,product_id, **kwargs) -> Optional[ProductModel]: 
        """
        Actualiza la información de un producto.

        Args:
            product_id (str): ID del producto a actualizar.
            name (Optional[str]): Nuevo nombre del producto (opcional).            

        Returns:
            Optional[ProductModel]: producto actualizado o None si no se encontró.
        """
        try:
            product =self.get_product_by_id(product_id)
            
            if product:
                product.name = kwargs.get("name")
                product.description = kwargs.get("description")
                product.sale_price = kwargs.get("sale_price")
                product.stock = kwargs.get("stock")
                product.created_at = kwargs.get("created_at")               


                return self.product_repo.save(product)
        except SQLAlchemyError as e:            
            raise e


    def delete_product(self, product_id: str) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id (str): ID del producto a eliminar.

        Returns:
            bool: True si el producto fue eliminado, False si no existe.
        """
        try:
            # Verificar que el producto exista
            product = self.get_product_by_id(str(product_id))
            # Eliminar producto
            return self.product_repo.delete(product)
        except SQLAlchemyError as e:
            raise e



    def update_product_stock(self, product_id: str, stock: int):
        if not product_id:
            raise ValidationError("El ID del producto es requerido.")

        product = self.get_product_by_id(product_id)

        if not product:
            raise NotFoundError("Producto no encontrado.")

        product.stock = stock
        return self.product_repo.save(product)