import os
from pymongo import MongoClient
from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection	
from config import db
from models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

router= APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_collection: Collection = db["users"]

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = users_collection.find_one({"email": user_email})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
@router.post("/register")
def register(user: User, token: str = None):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email bereits registriert")

    # Überprüfung der Rollen-Berechtigung
    if user.role in ["admin", "root"]:
        if not token:
            raise HTTPException(status_code=403, detail="Nur Admins oder Root können Admins erstellen")
        
        current_user = get_current_user(token)
        if current_user["role"] not in ["root"]:  # Nur Root kann Admins erstellen
            raise HTTPException(status_code=403, detail="Nicht autorisiert! Nur Root kann Admins erstellen")

    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password

    user_collection.insert_one(user_dict)
    return {"message": f"Benutzer {user.email} wurde erfolgreich erstellt", "role": user.role}

@router.post("/login")
def login(user: User):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Ungültige Anmeldeinformationen")

    access_token = create_access_token(
        data={"sub": db_user["email"], "role": db_user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}