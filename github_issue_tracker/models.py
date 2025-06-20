from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Issues(Base):
    __tablename__ = 'git_issues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    body = Column(String(1000))
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)