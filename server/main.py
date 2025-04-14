# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# from routes import auth, pdf, protected
# import uvicorn
# import subprocess
# import os
# import sys
# from pdf_watcher import start_pdf_watcher
# from motor.motor_asyncio import AsyncIOMotorClient
# import shutil

# # MongoDB-Verbindung
# MONGO_DETAILS = "mongodb://localhost:27017"  # Ändere dies, falls deine DB woanders läuft
# DB_NAME = "payroll_db"
# USER_COLLECTION = "users"

# # MongoDB-Client und Datenbank
# client = AsyncIOMotorClient(MONGO_DETAILS)
# db = client[DB_NAME]
# user_collection = db[USER_COLLECTION]

# # FastAPI Initialisierung
# app = FastAPI()

# # CORS erlauben für dein Frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Absoluter Pfad dieses Scripts
# server_path = os.path.dirname(os.path.abspath(__file__))

# # Pfade für Watcher & Verzeichnisse
# pdf_watcher_path = r"C:\Users\SCHUTZschild\Desktop\PayrollSCHUTZschild\server\pdf_watcher.py"
# eingehende_pdfs = os.path.join(server_path, "eingehende_pdfs")
# verarbeitete_pdfs = os.path.join(server_path, "verarbeitete_pdfs")
# static_pdfs = os.path.join(server_path, "static", "pdfs")

# # Ordner sicherstellen
# os.makedirs(eingehende_pdfs, exist_ok=True)
# os.makedirs(verarbeitete_pdfs, exist_ok=True)
# os.makedirs(static_pdfs, exist_ok=True)

# # Static Ordner korrekt einbinden unter "/static"
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # PDF-Watcher starten, falls vorhanden
# if os.path.exists(pdf_watcher_path):
#     try:
#         # Subprocess startet direkt im Verzeichnis "eingehende_pdfs"
#         subprocess.Popen([sys.executable, pdf_watcher_path], cwd=eingehende_pdfs)
#         print(f"✅ PDF-Watcher gestartet: {pdf_watcher_path}")
#     except Exception as e:
#         print(f"❌ Fehler beim Starten von pdf_watcher.py: {e}")
# else:
#     print(f"❌ Fehler: {pdf_watcher_path} nicht gefunden!")

# # Routen registrieren
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
# app.include_router(protected.router, prefix="/protected", tags=["Protected"])

# # Hilfsfunktion zum Abrufen eines Benutzers aus MongoDB
# async def get_user_from_db(user_id: str):
#     user = await user_collection.find_one({"user_id": user_id})
#     return user

# # Hilfsfunktion zum Extrahieren des Usernamens aus dem Dateinamen
# def get_user_from_filename(filename: str) -> str:
#     # Angenommen, der Dateiname enthält die User-ID z. B. "user123_gehaltsabrechnung.pdf"
#     user_id = filename.split("_")[0]
#     return user_id

# # PDF-Dateien analysieren und zuordnen
# @app.get("/assign_pdfs")
# async def assign_pdfs():
#     # Alle PDFs im Eingangsordner durchsuchen
#     for filename in os.listdir(eingehende_pdfs):
#         if filename.endswith(".pdf"):
#             user_id = get_user_from_filename(filename)
#             user = await get_user_from_db(user_id)  # User aus DB abfragen
#             if user:
#                 # Zielordner für den User erstellen, falls noch nicht vorhanden
#                 user_folder = os.path.join(static_pdfs, user_id)
#                 os.makedirs(user_folder, exist_ok=True)
                
#                 # Datei verschieben
#                 pdf_path = os.path.join(eingehende_pdfs, filename)
#                 target_path = os.path.join(user_folder, filename)
#                 shutil.move(pdf_path, target_path)
#                 print(f"PDF {filename} wurde {user['user_id']} zugewiesen.")
#             else:
#                 print(f"User mit ID {user_id} nicht gefunden.")
#     return {"message": "PDFs wurden verarbeitet und zugewiesen."}

# # Gehaltsabrechnungen für einen User bereitstellen
# @app.get("/user/{user_id}/pdfs")
# async def get_user_pdfs(user_id: str):
#     # Überprüfen, ob der User existiert
#     user = await get_user_from_db(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User nicht gefunden")

#     # Alle PDFs des Users zurückgeben
#     user_folder = os.path.join(static_pdfs, user_id)
#     if not os.path.exists(user_folder):
#         raise HTTPException(status_code=404, detail="Keine PDFs für diesen User gefunden")

#     pdf_files = [f for f in os.listdir(user_folder) if f.endswith(".pdf")]
#     if not pdf_files:
#         raise HTTPException(status_code=404, detail="Keine Gehaltsabrechnungen gefunden")

#     # Rückgabe der Dateinamen der PDFs
#     return {"pdf_files": pdf_files}

# @app.get("/")
# def root():
#     return {"message": "SCHUTZschild API läuft!"}

# @app.get("/start_pdf_watcher")
# def start_watcher(pdf_folder: str = "server/eingehende_pdfs"):
#     return start_pdf_watcher(pdf_folder)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import os
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from routes import auth, pdf, protected
import uvicorn

# MongoDB-Verbindung
MONGO_DETAILS = "mongodb://localhost:27017"  # DB-Verbindung zur MongoDB
DB_NAME = "payroll_db"
USER_COLLECTION = "users"

# MongoDB-Client und Datenbank
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client[DB_NAME]
user_collection = db[USER_COLLECTION]

# FastAPI Initialisierung
app = FastAPI()

# CORS erlauben für dein Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Absoluter Pfad dieses Scripts
server_path = os.path.dirname(os.path.abspath(__file__))

# Pfade für Watcher & Verzeichnisse
eingehende_pdfs = os.path.join(server_path, "eingehende_pdfs")
verarbeitete_pdfs = os.path.join(server_path, "verarbeitete_pdfs")
static_pdfs = os.path.join(server_path, "static", "pdfs")

# Ordner sicherstellen
os.makedirs(eingehende_pdfs, exist_ok=True)
os.makedirs(verarbeitete_pdfs, exist_ok=True)
os.makedirs(static_pdfs, exist_ok=True)

# Static Ordner korrekt einbinden unter "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Hilfsfunktion zum Abrufen eines Benutzers aus MongoDB
async def get_user_from_db(user_id: str):
    user = await user_collection.find_one({"user_id": user_id})
    return user

# Hilfsfunktion zum Extrahieren des Usernamens aus dem Dateinamen
def get_user_from_filename(filename: str) -> str:
    # Angenommen, der Dateiname enthält die User-ID z. B. "user123_gehaltsabrechnung.pdf"
    user_id = filename.split("_")[0]
    return user_id

# PDF-Dateien analysieren und zuordnen
@app.get("/assign_pdfs")
async def assign_pdfs():
    # Alle PDFs im Eingangsordner durchsuchen
    for filename in os.listdir(eingehende_pdfs):
        if filename.endswith(".pdf"):
            user_id = get_user_from_filename(filename)
            user = await get_user_from_db(user_id)  # User aus DB abfragen
            if user:
                # Zielordner für den User erstellen, falls noch nicht vorhanden
                user_folder = os.path.join(static_pdfs, user_id)
                os.makedirs(user_folder, exist_ok=True)
                
                # Datei verschieben
                pdf_path = os.path.join(eingehende_pdfs, filename)
                target_path = os.path.join(user_folder, filename)
                shutil.move(pdf_path, target_path)
                print(f"PDF {filename} wurde {user['user_id']} zugewiesen.")
            else:
                print(f"User mit ID {user_id} nicht gefunden.")
    return {"message": "PDFs wurden verarbeitet und zugewiesen."}

# Gehaltsabrechnungen für einen User bereitstellen
@app.get("/user/{user_id}/pdfs")
async def get_user_pdfs(user_id: str):
    # Überprüfen, ob der User existiert
    user = await get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User nicht gefunden")

    # Alle PDFs des Users zurückgeben
    user_folder = os.path.join(static_pdfs, user_id)
    if not os.path.exists(user_folder):
        raise HTTPException(status_code=404, detail="Keine PDFs für diesen User gefunden")

    pdf_files = [f for f in os.listdir(user_folder) if f.endswith(".pdf")]
    if not pdf_files:
        raise HTTPException(status_code=404, detail="Keine Gehaltsabrechnungen gefunden")

    # Rückgabe der Dateinamen der PDFs
    return {"pdf_files": pdf_files}

# Routen registrieren
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

@app.get("/")
def root():
    return {"message": "SCHUTZschild API läuft!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
