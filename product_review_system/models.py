from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, TEXT, ForeignKey


class products(Base):

    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(TEXT)
    price = Column(Integer)
    review = relationship("reviews", back_populates="product", cascade="all, delete")


class reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)
    comments = Column(String)
    author = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("products", back_populates="review")


