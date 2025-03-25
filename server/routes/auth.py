import os
from pymongo import MongoClient, errors
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Request
from pymongo.collection import Collection	
from config import db
from models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

try:
    user_collection: Collection = db["users"]
except errors.PyMongoError as e:
    raise RuntimeError(f"Fehler beim Verbinden mit der Datenbank: {e}")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token-Erstellung fehlgeschlagen: {str(e)}")

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Ungültige Authentifizierungsdaten")
        
        user = user_collection.find_one({"email": user_email})
        if user is None:
            raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Ungültiger Token")
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")

@router.get("/me")
def get_me(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token fehlt oder ist ungültig")
    
    token = token.split("Bearer ")[1]  # Entfernt "Bearer " und gibt den eigentlichen Token weiter
    user = get_current_user(token)  # Hier sollte die JWT-Verarbeitung erfolgen

    return {
        "email": user["email"],
        "full_name": user.get("full_name", "Unbekannt"),
        "role": user["role"]
    }

@router.get("/users")
def get_users(token: str):
    current_user = get_current_user(token)
    if current_user.get("role") not in ["admin", "root"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert!")
    users = list(user_collection.find({}, {"password": 0}))
    return users

@router.get("/users/{user_id}")
def get_user(user_id: str, token: str):
    current_user = get_current_user(token)
    if current_user.get("role") not in ["admin", "root"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert!")
    user = user_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    return user

@router.put("/profile")
def update_profile(user: User, token: str):
    current_user = get_current_user(token)
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    user_collection.update_one({"email": current_user["email"]}, {"$set": update_data})
    return {"message": "Profil erfolgreich aktualisiert"}

@router.post("/register")
def register(user: User, token: str = None):
    try:
        if user_collection.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

        if user.role in ["admin", "root"]:
            if not token:
                raise HTTPException(status_code=403, detail="Nur Admins oder Root können Admins erstellen")
            
            current_user = get_current_user(token)
            if current_user.get("role") != "root":
                raise HTTPException(status_code=403, detail="Nicht autorisiert! Nur Root kann Admins erstellen")

        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict["password"] = hashed_password
        
        user_collection.insert_one(user_dict)
        return {"message": f"Benutzer {user.full_name} wurde erfolgreich erstellt", "role": user.role}
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unbekannter Fehler: {str(e)}")


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(user: LoginRequest):
    try:
        db_user = user_collection.find_one({"email": user.email})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Ungültige Anmeldeinformationen")

        access_token = create_access_token(
            data={"sub": db_user["email"], "role": db_user["role"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unbekannter Fehler: {str(e)}")
