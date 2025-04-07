from pydantic import BaseModel, EmailStr
from typing import List, Literal

class User(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Literal["user", "admin", "root"] = "user"  # Standardmäßig "user"
    assigned_pdfs: List[str] = []  # Liste von PDF-Dateinamen, die dem Benutzer zugewiesen wurden

    class Config:
        from_attributes = True  # Pydantic V2: Verwendung von 'from_attributes' anstelle von 'orm_mode'
