from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    _id: ObjectId
    email: str
    name: str
    provider: str
    provider_id: str
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    email: str
    name: str
    provider: str
    provider_id: str
    created_at: datetime
    updated_at: datetime

class UserOut(BaseModel):
    _id: ObjectId
    email: str
    name: str
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    
class UserUpdate(BaseModel):
    name: str
    updated_at: datetime
