# Reaktion 1
**Erinnerung aktualisiert**

Super, dein Code ist bereits gut strukturiert! Hier sind einige mögliche Verbesserungen und Ergänzungen:

### 1️⃣ Fehlende Abhängigkeiten in `get_current_user`
In `get_current_user` fehlt `Depends()`, um den Token aus der Anfrage zu extrahieren:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
```

### 2️⃣ Umwandlung von `ObjectId` in `str` bei der Benutzerliste
MongoDB gibt `ObjectId`-Objekte zurück, die nicht direkt in JSON serialisiert werden können. Nutze `str()`:

```python
users = list(user_collection.find({}, {"password": 0}))
for user in users:
    user["_id"] = str(user["_id"])
return users
```

### 3️⃣ Berechtigungsprüfung für `update_profile` verbessern
Nur der angemeldete Nutzer soll sein eigenes Profil ändern dürfen:

```python
if current_user["email"] != user.email and current_user["role"] != "root":
    raise HTTPException(status_code=403, detail="Du kannst nur dein eigenes Profil bearbeiten!")
```

### 4️⃣ Rollenbasierte Routen zu `protected.py` verschieben
Die Admin- und Root-Endpunkte können sauberer in `protected.py` verwaltet werden.

---