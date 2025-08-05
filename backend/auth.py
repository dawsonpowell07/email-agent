"""Authentication utilities for verifying Google OAuth tokens."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Iterator, Optional

from fastapi import Depends, HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlmodel import SQLModel, Field, Session, create_engine, select

from .schemas import AgentRequest

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class User(SQLModel, table=True):
    """Database model representing an authenticated user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    google_sub: str
    token_expiry: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)


def create_db_and_tables() -> None:
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Yield a SQLModel session."""
    with Session(engine) as session:
        yield session


logger = logging.getLogger(__name__)


def verify_token(token_info: str, session: Session) -> User:
    """Validate the provided OAuth token and persist the user.

    Args:
        token_info: Raw OAuth token JSON string from the client.
        session: Database session.

    Returns:
        A ``User`` instance representing the authenticated user.

    Raises:
        HTTPException: If the token is missing or invalid.
    """
    if not token_info:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        info = json.loads(token_info)
        raw_token = info.get("token") or info.get("id_token")
        if raw_token is None:
            raise ValueError("token field missing")
        idinfo = id_token.verify_oauth2_token(
            raw_token, requests.Request(), info.get("client_id")
        )
    except (
        ValueError,
        json.JSONDecodeError,
    ) as exc:  # pragma: no cover - broad except for robustness
        logger.exception("Token verification failed: %s", exc)
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    email = idinfo.get("email")
    sub = idinfo.get("sub")
    expiry = datetime.fromtimestamp(idinfo.get("exp", 0))

    user = session.exec(select(User).where(User.google_sub == sub)).first()
    if user is None:
        user = User(email=email, google_sub=sub, token_expiry=expiry)
        session.add(user)
    else:
        user.email = email
        user.token_expiry = expiry
    session.commit()

    logger.info("Authenticated user %s", email)
    return user


def get_current_user(
    request: AgentRequest, session: Session = Depends(get_session)
) -> User:
    """FastAPI dependency that authenticates the request and returns the user."""
    return verify_token(request.token_info, session)
