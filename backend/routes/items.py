from fastapi import APIRouter, HTTPException
from typing import List
from models import Item
from db import init_db
from bson import ObjectId

router = APIRouter()


async def get_items_collection():
    return init_db()["items_collection"]


@router.get("/", response_model=List[Item])
async def read_items():
    collection = await get_items_collection()
    items = []
    async for item in collection.find():
        item["_id"] = str(item["_id"])
        items.append(Item(**item))
    return items


@router.post("/", response_model=Item)
async def create_item(item: Item):
    collection = await get_items_collection()
    item_dict = item.dict()
    result = await collection.insert_one(item_dict)
    created_item = await collection.find_one({"_id": result.inserted_id})
    if created_item:
        created_item["_id"] = str(created_item["_id"])
        return Item(**created_item)
    raise HTTPException(status_code=500, detail="Item could not be created")


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    collection = await get_items_collection()
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
