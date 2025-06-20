from typing import Annotated, Dict, Optional
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status

import models
from models import records
from database import engine, sessionlocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class getdata(BaseModel):
    name: str=Field(...,min_length=4,max_length=50)
    department: str=Field(...,min_length=4,max_length=50)
    cgpa: float=Field(...,gt=-1,lt=4)

class updatedata(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    cgpa: Optional[float] = Field(default=None, gt=-1, lt=4)



#Get Methods
@app.get('/')
def get_data(db:db_dependency):
    return 'Welcome to Students Record'

@app.get('/allrecords')
def get_data(db:db_dependency):
    return db.query(records).all()

@app.get('/record/sorted-by-cgpa',status_code=status.HTTP_200_OK)
def get_sorted_rec(db:db_dependency):
    return sorted(db.query(records).all(),key=lambda r:r.cgpa)

@app.get('/record/{st_id}',status_code=status.HTTP_200_OK)
def get_record_id(db:db_dependency, st_id:int=Path(...,gt=-1)):
     model = db.query(records).filter(st_id == records.id).first()
     if model is not None:
         return model
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#post methods
@app.post('/addrecord',status_code=status.HTTP_201_CREATED)
def add_record(db:db_dependency, data:updatedata):
    model = records(**data.dict())

    db.add(model)
    db.commit()


#put method
@app.put('/updaterecord/{st_id}',status_code=status.HTTP_204_NO_CONTENT)
def update_record(db:db_dependency, st_id:int,data:updatedata):
    model = db.query(records).filter(st_id == records.id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if data.name is not None:
        model.name = data.name
    if data.department is not None:
        model.department = data.department
    if data.cgpa is not None:
        model.cgpa = data.cgpa


    db.add(model)
    db.commit()



#delete methods
@app.delete('/deleterecord/{st_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_record(db:db_dependency, st_id:int):
    model = db.query(records).filter(st_id == records.id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(model)
    db.commit()