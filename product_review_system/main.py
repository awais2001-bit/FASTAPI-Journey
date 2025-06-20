from typing import Annotated, Optional
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, Body
from starlette import status

import models
from models import products,reviews
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

class newprod(BaseModel):
    name: str=Field(...,min_length=3,max_length=15)
    description: str=Field(...,min_length=3,max_length=500)
    price: int=Field(...,gt=0)

class updateprod(BaseModel):
    name: Optional[str]=Field(None,min_length=3,max_length=15)
    description: Optional[str]=Field(None,min_length=3,max_length=500)
    price: Optional[int]=Field(None,gt=0)

class newreview(BaseModel):
    rating: float=Field(...,gt=-1)
    comments: str=Field(...,min_length=3,max_length=500)
    author: str=Field(...,min_length=3,max_length=15)
    product_id: int=Field(...,gt=0)

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/products')
def all_products(db: db_dependency):
    return db.query(products).all()

@app.get('/products/{prod_id}',status_code=status.HTTP_200_OK)
def get_product(prod_id: int,db: db_dependency):
    db_model = db.query(products).filter(products.id == prod_id).first()
    if db_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_model


@app.get('/products/{prod_id}/reviews',status_code=status.HTTP_200_OK)
def get_reviews(prod_id: int,db: db_dependency):
    db_model = db.query(reviews).filter(reviews.product_id == prod_id).all()
    if db_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_model

@app.get('/products/reviews/{min_review}',status_code=status.HTTP_200_OK)
def get_products_by_reviews(db: db_dependency,min_review: float=Path(gt=-1,lt=5)):
    products_ratingwise = db.query(products).join (reviews).filter(reviews.rating < min_review).all()
    return products_ratingwise



@app.post('/addproduct',status_code=status.HTTP_201_CREATED)
def add_product(db: db_dependency, product: newprod):
    new_product = products(**product.dict())

    db.add(new_product)
    db.commit()


@app.post('/addreview',status_code=status.HTTP_201_CREATED)
def add_review(db: db_dependency, review: newreview):
    new_review = reviews(**review.dict())

    db.add(new_review)
    db.commit()

@app.put('/updateproduct/{prod_id}',status_code=status.HTTP_204_NO_CONTENT)
def update_product(db: db_dependency, prod_id: int,product: updateprod=Body(...)):

    updated_product = db.query(products).filter(products.id == prod_id).first()

    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if product.name is not None:
        updated_product.name = product.name
    if product.description is not None:
        updated_product.description = product.description
    if product.price is not None:
        updated_product.price = product.price

    db.add(updated_product)
    db.commit()


@app.delete('/deleteproduct/{prod_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_product(db: db_dependency, prod_id: int):
    deleted_product = db.query(products).filter(products.id == prod_id).first()
    if deleted_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(deleted_product)
    db.commit()


@app.delete('/product/{product_id}/ereview/{review_id}',status_code=status.HTTP_204_NO_CONTENT)
def del_specific_review(db: db_dependency, review_id: int,product_id: int):
    deleted_review = db.query(reviews).filter(reviews.id == review_id, reviews.product_id== product_id).first()

    if deleted_review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(deleted_review)
    db.commit()


