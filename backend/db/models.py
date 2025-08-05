from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from .session import Base


class User(Base):
    """SQLAlchemy model for application users."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    name: str = Column(String, nullable=False)
    role: str = Column(String, default="user", nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
