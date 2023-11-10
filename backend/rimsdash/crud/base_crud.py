from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from rimsdash.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).get(id)
            #get searches against the primary key, not necessarily called "id"

    def get_all(self, db: Session) -> Optional[ModelType]:
        return db.query(self.model).all()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 5000) -> List[ModelType]:
        return (
            db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        )

    def create(self, db: Session, obj_in: CreateSchemaType):

        #encode the schema as dict
        in_data = jsonable_encoder(obj_in)  
        #      ALT: obj_in.dict(exclude_unset=True)
        
        #create a database object using model and the schema dict
        db_obj = self.model(**in_data)

        #add that object and update
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType):
     
        db_data = jsonable_encoder(db_obj)
        in_data = jsonable_encoder(obj_in)        

        #iterate db fields, setting by input
        for field in db_data:
            if field in in_data:
                setattr(db_obj, field, in_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def delete(self, db: Session, id: int):
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()

    def drop_table(self, db: Session):
        db.query(self.model).delete()