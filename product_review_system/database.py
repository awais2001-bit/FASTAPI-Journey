from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlalchemy_database_url = 'sqlite:///./prod_rev.db'

engine = create_engine(sqlalchemy_database_url, connect_args={"check_same_thread": False})

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




