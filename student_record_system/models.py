from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, TEXT


class records(Base):

    __tablename__ = 'students_rec'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    cgpa = Column(Float)

