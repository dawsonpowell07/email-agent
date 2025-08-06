from backend.db.db import get_database
from backend.db.models import UserCreate, UserOut, UserUpdate
from bson import ObjectId

async def create_user(user: UserCreate) -> UserOut:
    try:
        db = get_database()
        
        user_collection = db["users"]
        
        result = await user_collection.insert_one(user.dict())
        
        return UserOut(
            _id = result.inserted_id,
            email=user.email,
            name=user.name,
        )
    
    except Exception as e:
        raise Exception(f"Error creating user: {e}")

async def get_user_by_email(email: str) -> UserOut | None:
    try:
        db = get_database()
        
        user_collection = db["users"]
        
        user = await user_collection.find_one({"email": email})
        
        if user:
            return UserOut(
                _id = user["_id"],
                email=user["email"],
                name=user["name"],
            )
        
        return None
    
    except Exception as e:
        raise Exception(f"Error getting user by email: {e}")
    
async def get_user_by_id(user_id: str) -> UserOut | None:
    try:
        db = get_database()
        
        user_collection = db["users"]
        
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        
        if user:
            return UserOut(
                _id = user["_id"],    
                email=user["email"],
                name=user["name"],
            )
        return None
    except Exception as e:
        raise Exception(f"Error getting user by id: {e}")
    
async def update_user(user_id: str, user: UserUpdate) -> UserOut | None:
    try:
        db = get_database()
        
        user_collection = db["users"]
        
        result = await user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"name": user.name, "updated_at": user.updated_at}}
        )
        
        if result.modified_count == 1:
            updated_user = await user_collection.find_one({"_id": ObjectId(user_id)})
            return UserOut(
                _id = updated_user["_id"],
                email=updated_user["email"],
                name=updated_user["name"],
            )
        return None
    except Exception as e:
        raise Exception(f"Error updating user: {e}")
    
async def delete_user(user_id: str) -> bool:
    try:
        db = get_database()
        
        user_collection = db["users"]
        
        result = await user_collection.delete_one({"_id": user_id})
        
        return result.deleted_count == 1
    except Exception as e:
        raise Exception(f"Error deleting user: {e}")