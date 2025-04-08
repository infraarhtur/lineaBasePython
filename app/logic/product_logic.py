import json
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.category_repository import CategoryRepository
from app.data.product_repository import ProductRepository
from app.models.category_model import CategoryModel
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
            self.category_repo = CategoryRepository(self.db)
    
    def __delete__(self):
        """Cierra la sesión automáticamente cuando se destruye la instancia"""
        if self.db is not None :
            self.db.close()

    def create_product(self, **kwargs) -> ProductModel:
        """
        Crea un nuevo producto con sus categorías asociadas.

        Args:
            **kwargs: Campos del producto (incluye category_ids opcional).

        Returns:
            ProductModel: Producto creado.

        Raises:
            ValidationError: Si los datos son inválidos.
            SQLAlchemyError: Si ocurre error en base de datos.
        """
        try:
            name = kwargs.get("name")
            category_ids = kwargs.get("category_ids", [])
            # Validar campos obligatorios
            if not name:
                raise ValidationError(const.ERROR_MISSING_REQUIRED_FIELDS)
            
        # Cargar las categorías si hay IDs
            categories = []
            if category_ids:
                for category_id in category_ids:
                    category = self.category_repo.fetch(category_id)
                    if not category:
                        raise ValidationError(f"Categoría con ID {category_id} no encontrada.")
                    categories.append(category)

                    # Crear el producto
            product = ProductModel(
                name=name,
                description=kwargs.get("description"),
                sale_price=kwargs.get("sale_price"),
                purchase_price=kwargs.get("purchase_price"),
                stock=kwargs.get("stock"),
                created_at= datetime.utcnow(),
                categories=categories  # Asociar categorías
            )          

            
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
            product = self.product_repo.fetch_by_id(product_id)            
            
        except SQLAlchemyError as e:
            raise e

        if not product:
            product_id = str(product_id)
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

            category_ids = kwargs.get("category_ids")
            if category_ids is not None:
                categories = []
            for category_id in category_ids:
                category = self.category_repo.fetch(category_id)
                if not category:
                    raise ValidationError(f"Categoría con ID {category_id} no encontrada.")
                categories.append(category)
            product.categories = categories  # Se reemplazan todas las categorías             


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
        # Validar que sea un UUID válido

        try:
            
            # Verificar que el producto exista
            product = self.get_product_by_id(str(product_id))
            # if not product:
            #     raise NotFoundError(f"Producto con ID {product_id} no encontrado.")
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