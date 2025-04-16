from fastapi import APIRouter, HTTPException
from models import User
from bson import ObjectId

router = APIRouter()

async def get_users_collection():
    from db import init_db
    return init_db()["users_collection"]


# 💡 Use GET for fetching users
@router.get("/")
async def get_users():
    collection = await get_users_collection()
    users = []
    async for user in collection.find():
        user["_id"] = str(user["_id"])  # Serialize ObjectId
        users.append(user)
    return users


# ✅ POST for creating a user
@router.post("/")
async def create_user(user: User):
    collection = await get_users_collection()
    result = await collection.insert_one(user.dict(by_alias=True))  # Ensures _id gets mapped properly
    return {"id": str(result.inserted_id)}


# ✅ DELETE by user_id
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    collection = await get_users_collection()
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="User not found")
