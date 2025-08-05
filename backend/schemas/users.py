from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str = "user"


class UserCreate(UserBase):
    """Schema for creating users."""


class UserRead(UserBase):
    """Schema for reading users."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating users."""

    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[str] = None
