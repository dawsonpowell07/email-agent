from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.db.session import Base, get_db
from backend.db import models
from backend.api.auth.users import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    db = TestingSessionLocal()
    try:
        return db.query(models.User).first()
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_user_crud_flow():
    response = client.post(
        "/api/authentication/users/",
        json={"email": "test@example.com", "name": "Test", "role": "user"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    user_id = data["id"]

    response = client.get(f"/api/authentication/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

    response = client.put(
        f"/api/authentication/users/{user_id}",
        json={"name": "Updated"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

    response = client.delete(f"/api/authentication/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/api/authentication/users/{user_id}")
    assert response.status_code == 404


def test_unauthorized_access():
    db = TestingSessionLocal()
    user1 = models.User(email="a@example.com", name="A", role="user")
    user2 = models.User(email="b@example.com", name="B", role="user")
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    db.close()

    def override_current_user_b():
        db = TestingSessionLocal()
        try:
            return (
                db.query(models.User)
                .filter(models.User.email == "b@example.com")
                .first()
            )
        finally:
            db.close()

    app.dependency_overrides[get_current_user] = override_current_user_b
    response = client.put(
        f"/api/authentication/users/{user1.id}",
        json={"name": "Hack"},
    )
    assert response.status_code == 403
