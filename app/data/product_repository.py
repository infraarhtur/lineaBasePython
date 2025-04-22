import uuid
from typing import List, Optional, cast

import psycopg2
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.category_model import CategoryModel
from app.models.product_provider_model import ProductProviderModel
from app.models.products_model import ProductModel


class ProductRepository:
    """
    Clase que define las operaciones de repositorio para el modelo ProductModel.
    Se encarga de manejar la lógica de acceso a datos mediante SQLAlchemy.
    """
    def __init__(self, db: Session):
        """
        Constructor de la clase ProductRepository.
        
        Args:
            db (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db



    def save(self, product: ProductModel) -> ProductModel:
        """
        Guarda un producto en la base de datos.

        Args:
            product (ProductModel): Instancia del producto a guardar.

        Returns:
            ProductModel: Instancia del producto guardado con su ID actualizado.

        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación.
        """
        try:
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return product
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

        
    def fetch_by_id(self, product_id: uuid.UUID) -> Optional[ProductModel]:
        """
        Recupera un producto de la base de datos por su ID,
        incluyendo las categorías asociadas.

        Args:
            product_id (uuid.UUID): ID del producto.

        Returns:
            Optional[ProductModel]: Producto encontrado o None.
        """
        try:
            if self.db.in_transaction():
                self.db.rollback()

            query = (
                self.db.query(ProductModel)
                .options(joinedload(ProductModel.categories),                         
                    joinedload(ProductModel.providers),
                    joinedload(ProductModel.product_providers))
                .filter(ProductModel.id == product_id)
            )

            print("🧪 SQL generado:", query.statement.compile(
                dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

            return query.first()

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"❌ Error SQLAlchemy al recuperar producto con ID {product_id}: {e}")
            raise e

    def fetch_all(self) -> List[ProductModel]:
        try:
            query = (
                self.db.query(ProductModel)
                .options(
                    joinedload(ProductModel.categories),
                    joinedload(ProductModel.providers),
                    joinedload(ProductModel.product_providers)
                )
            )
            print("🧪 SQL:", query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
            return query.all()

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"❌ Error al obtener todos los productos: {e}")
            raise e

    def delete(self, product: ProductModel) -> bool:
        """
        Elimina un producto de la base de datos por su ID.

        Args:
            product_id (str): ID del product a eliminar.

        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación en la base de datos.
        """
        try:
            if not product:
                raise ValueError(f"product con ID {product.id} no encontrado.")

            # Eliminar el Producto
            self.db.delete(product)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()  # Revertir la transacción si ocurre un error
            raise e
        

    def fetch_by_category_id(self, category_id: uuid.UUID) -> List[ProductModel]:
        """
        Obtiene todos los productos asociados a una categoría específica.

        Args:
            category_id (uuid.UUID): ID de la categoría.

        Returns:
            List[ProductModel]: Lista de productos.
        """
        try:
            query = (
                self.db.query(ProductModel)
                .join(ProductModel.categories)
                .filter(CategoryModel.id == category_id)
                
            )
            print(query.statement.compile(dialect=postgresql.dialect(),
                                           compile_kwargs={"literal_binds": True}))
            return query.all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
