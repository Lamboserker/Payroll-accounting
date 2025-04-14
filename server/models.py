from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    user_id: str
    name: str
    email: str

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }

class UserInDB(User):
    hashed_password: str
