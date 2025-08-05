from sqlalchemy.orm import Session
from typing import Optional
from . import models
from backend.schemas.users import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> models.User:
    """Create a new user."""
    db_user = models.User(email=user.email, name=user.name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Retrieve a user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Retrieve a user by id."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, db_user: models.User, updates: UserUpdate) -> models.User:
    """Update an existing user."""
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: models.User) -> None:
    """Delete a user."""
    db.delete(db_user)
    db.commit()
