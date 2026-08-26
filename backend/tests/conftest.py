import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db
from app.services.seed import seed_database

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_food_freshness.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def admin_token(client):
    res = client.post("/api/auth/login", json={
        "email": "admin@foodfreshness.com",
        "password": "Admin123!"
    })
    return res.json()["access_token"]

@pytest.fixture
def retail_token(client):
    res = client.post("/api/auth/login", json={
        "email": "retail@foodfreshness.com",
        "password": "Manager123!"
    })
    return res.json()["access_token"]

@pytest.fixture
def consumer_token(client):
    res = client.post("/api/auth/login", json={
        "email": "consumer@foodfreshness.com",
        "password": "Consumer123!"
    })
    return res.json()["access_token"]
