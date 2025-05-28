import uuid
from typing import List, Optional

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

# from app.models.sale_model import SaleDetailModel  # Asegúrate de tenerlo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.client_model import ClientModel
from app.models.sale_model import SaleModel


class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, sale: SaleModel) -> SaleModel:

        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def get_all(self) -> List[SaleModel]: 
        query = self.db.query(SaleModel).options(joinedload(SaleModel.client))
        print(query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return query.all()


    def get_by_id(self, sale_id: uuid.UUID) -> Optional[SaleModel]:
        
        query =self.db.query(SaleModel).filter(SaleModel.id == sale_id)
        print(query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return query.first()

    def delete(self, sale: SaleModel) -> bool:
        try:
            self.db.delete(sale)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            return False
