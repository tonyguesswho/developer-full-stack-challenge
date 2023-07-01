from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID

from core.database import Base
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)


class BaseManager(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get_all(self, db: Session) -> Optional[List[ModelType]]:
        return db.query(self.model).all()

    def get_all_by_ids(self, db: Session, ids: List[UUID]) -> Optional[List[ModelType]]:
        if ids is None:
            ids = []
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

    def get_by_id(self, db: Session, id: UUID) -> Optional[ModelType]:
        return db.query(self.model).filter_by(id=id).first()

    def get(
        self, db: Session, offset: int = 0, limit: int = 100
    ) -> Optional[List[ModelType]]:
        return db.query(self.model).offset(offset).limit(limit).all()

    def create(self, db: Session, obj_in: Optional[ModelType]) -> Optional[ModelType]:
        if not obj_in:
            return None
        obj_in["created_at"] = datetime.utcnow()
        obj_in["updated_at"] = obj_in["created_at"]
        obj = self.model(**obj_in)

        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def bulk_create(self, db: Session, obj_in: List[ModelType]) -> Optional[List]:
        items = db.execute(
            insert(self.model)
            .values(obj_in)
            .on_conflict_do_nothing()
            .returning(self.model.id)
        )
        db.commit()
        ids = [item[0] for item in items]
        return ids

    def update(
        self, db: Session, db_obj: Optional[ModelType], obj_in: Optional[ModelType]
    ) -> Optional[ModelType]:
        if not db_obj:
            return None
        for attr, value in obj_in.items():
            setattr(db_obj, attr, value)
        db_obj.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Optional[ModelType]):
        if db_obj:
            db.delete(db_obj)
            db.commit()

    def delete_by_id(self, db: Session, id: UUID):
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
