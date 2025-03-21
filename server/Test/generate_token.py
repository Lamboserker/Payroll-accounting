from datetime import datetime, timedelta
from jose import jwt

# Dein geheimer Schlüssel
SECRET_KEY = "34ß09593450897ß5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Beispiel-Nutzerdaten
user_data = {
    "sub": "root@example.com",
    "role": "root"
}

# Token generieren
token = create_access_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
print(f"Dein Token: {token}")
