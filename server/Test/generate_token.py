import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

# Hole den geheimen Schlüssel aus der .env-Datei
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise ValueError("⚠️ ERROR: JWT_SECRET_KEY ist nicht in .env gesetzt!")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Erstellt ein JWT-Token mit einer optionalen Ablaufzeit."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """Dekodiert das JWT-Token und überprüft es."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ✅ Erstelle den Token für den Benutzer
user_data = {
    "sub": "lukaslamberz96@gmail.com",
    "password": "123456789",
    "role": "user"
}

token = create_access_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

print("\n✅ Token erfolgreich erstellt!")
print(f"🔑 Dein Token: {token}\n")

# ✅ Teste das Decodieren
decoded_data = decode_access_token(token)
if decoded_data:
    print("🔓 Token erfolgreich dekodiert:", decoded_data)
else:
    print("⛔ Fehler beim Dekodieren des Tokens!")
