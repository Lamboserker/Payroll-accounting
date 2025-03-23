from pydantic import BaseModel, EmailStr
from typing import Literal  # Korrekte Import-Anweisung

class User(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Literal["user", "admin", "root"] = "user"  # Standardmäßig "user"

    class Config:
        orm_mode = True