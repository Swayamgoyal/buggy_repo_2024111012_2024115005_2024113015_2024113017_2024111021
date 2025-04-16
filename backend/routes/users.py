from fastapi import APIRouter, HTTPException
from bson import ObjectId  # Import ObjectId
from models import User
from db import init_db

router = APIRouter()


async def get_users_collection():
    return init_db()["users_collection"]


@router.post("/", response_model=User)
async def create_user(user: User):
    collection = await get_users_collection()
    user_dict = user.dict()
    result = await collection.insert_one(user_dict)
    created_user = await collection.find_one({"_id": result.inserted_id})
    if created_user:
        created_user["_id"] = str(created_user["_id"])
        return created_user
    raise HTTPException(status_code=500, detail="User could not be created")


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str):
    collection = await get_users_collection()
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    collection = await get_users_collection()
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/profile")
async def get_user_profile():
    # Placeholder: Replace with actual logic to get current user
    return {"username": "dummyUser", "email": "dummy@example.com"}


@router.get("/stats")
async def get_user_stats():
    # Placeholder: Replace with actual logic
    return {"logins": 15, "last_login": "2025-04-16T10:00:00Z"}


@router.delete("/delete")
async def delete_current_user_account():
    # Placeholder: Replace with actual logic to delete the authenticated user
    print(f"Attempting to delete current user account...")
    return {"message": "Account deletion initiated (placeholder)"}
