from pydantic import BaseModel, Field  # Import BaseModel
from typing import Optional
from bson import ObjectId  # Import ObjectId if using MongoDB _id


# Helper for MongoDB ObjectId validation/serialization if needed
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator, _field_schema):
        # Updated from __modify_schema__ to __get_pydantic_json_schema__
        return {"type": "string"}


class Item(BaseModel):  # Inherit from BaseModel
    # Use PyObjectId for id if mapping directly to MongoDB _id
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        validate_by_name = True  # Updated from allow_population_by_field_name
        arbitrary_types_allowed = True  # Needed for ObjectId
        json_encoders = {ObjectId: str}


class User(BaseModel):  # Assuming a User model exists based on users.py
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    # Add other fields as necessary, e.g., hashed_password: str

    class Config:
        validate_by_name = True  # Updated from allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
