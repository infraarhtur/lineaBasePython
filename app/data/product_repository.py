import uuid
from typing import List, Optional, cast

import psycopg2
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

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

        

    def fetch(self, product_id: str) -> ProductModel:
        """
        Recupera un producto de la base de datos por su ID.
        
        Args:
            product_id (uuid.UUID): ID del producto a buscar.
        
        Returns:
            ProductModel: producto encontrado o None si no existe.
        """
        try:       
            # Si la sesión está en estado inválido, reiniciarla
            if self.db.in_transaction():
                self.db.rollback()

            query = self.db.query(ProductModel).filter(ProductModel.id == product_id)
            print(query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
           
            product = query.first()            

            return product
        except psycopg2.errors.InFailedSqlTransaction:
            print("⚠️ Transacción fallida detectada. Reiniciando sesión de base de datos...")
            self.db.rollback()
            product = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
            return product
        except SQLAlchemyError as e:
            if self.db.in_transaction():
                self.db.rollback()
            print(f"❌ Error SQLAlchemy al recuperar producto con ID {product_id}: {e}")
            raise e

    def fetch_all(self) -> List[ProductModel]:
        """
        Recupera todos los Productos de la base de datos.
        
        Returns:
            List[ProductModel]: Lista de todos los productos.
        
        Raises:
            SQLAlchemyError: Si ocurre un error durante la operación.
        """

        try:
            return self.db.query(ProductModel).all()
        except SQLAlchemyError as e:
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