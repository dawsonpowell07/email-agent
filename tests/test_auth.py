import json
import os

from fastapi.testclient import TestClient
from google.oauth2 import id_token
from sqlmodel import SQLModel, Session, create_engine, select

# configure in-memory database for tests
os.environ["DATABASE_URL"] = "sqlite://"

from backend.auth import User, verify_token  # noqa: E402
from backend.main import app  # noqa: E402


client = TestClient(app)


def test_verify_token_creates_user(monkeypatch):
    def fake_verify(token, request, audience=None):  # pragma: no cover - simple stub
        return {"email": "user@example.com", "sub": "abc", "exp": 32503680000}

    monkeypatch.setattr(id_token, "verify_oauth2_token", fake_verify)

    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        token_info = json.dumps({"token": "t", "client_id": "c"})
        user = verify_token(token_info, session)
        assert user.email == "user@example.com"
        db_user = session.exec(select(User)).first()
        assert db_user is not None


def test_label_requires_token():
    response = client.post("/label", json={"user_email": "a", "token_info": None})
    assert response.status_code == 401
