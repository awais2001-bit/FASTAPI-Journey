from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..routers.auth import get_db, get_user
from ..database import Base
from ..main import app
from ..routers import todos
from fastapi.testclient import TestClient





sqlalchemy_database_url = 'sqlite:///./testdb.db'




engine = create_engine(sqlalchemy_database_url,
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_user():
    return {'username':'ahmed2000','id':1,'role':'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user

client = TestClient(app)

def test_all():
    response = client.get('/to')
    assert response.status_code == 200


