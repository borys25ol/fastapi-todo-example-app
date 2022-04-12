from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from main.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository with basic methods.
    """

    def __init__(self, db: Session, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        :param db: A SQLAlchemy Session object.
        :param model: A SQLAlchemy model class.
        """
        self.db = db
        self.model = model

    def get_all(self) -> List[ModelType]:
        """
        Return all objects from specific db table.
        """
        return self.db.query(self.model).all()

    def get(self, obj_id: str) -> Optional[ModelType]:
        """
        Get object by `id` field.
        """
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, obj_create: CreateSchemaType) -> ModelType:
        """
        Create new object in db table.
        """
        obj = self.model(**obj_create.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType, obj_update: UpdateSchemaType) -> ModelType:
        """
        Update model object by fields from `obj_update` schema.
        """
        obj_data = jsonable_encoder(obj)
        update_data = obj_update.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj_id: int) -> Optional[ModelType]:
        """
        Delete object.
        """
        obj = self.db.query(self.model).get(obj_id)
        self.db.delete(obj)
        self.db.commit()
        return obj
