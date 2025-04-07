from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, pdf, protected
import uvicorn
import subprocess
import os
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Dein Frontend-Host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Absoluten Pfad zur Datei ermitteln
server_path = os.path.dirname(os.path.abspath(__file__))  
pdf_watcher_path = os.path.join(server_path, "pdf_watcher.py")


# Sicherstellen, dass der Ordner existiert
pdf_dir = "server/eingehende_pdfs"
os.makedirs(pdf_dir, exist_ok=True)

# Den Ordner als statisches Verzeichnis einbinden
app.mount("/pdfs", StaticFiles(directory=pdf_dir), name="pdfs")

# Python-Interpreter ermitteln (falls virtuelle Umgebung aktiv ist, diese bevorzugen)
python_path = sys.executable

# Überprüfen, ob `pdf_watcher.py` existiert
if os.path.exists(pdf_watcher_path):
    try:
        # Starte `pdf_watcher.py` im Hintergrund
        subprocess.Popen([python_path, pdf_watcher_path], cwd=server_path)
        print(f"✅ PDF-Watcher gestartet: {pdf_watcher_path} mit {python_path}")
    except Exception as e:
        print(f"❌ Fehler beim Starten von pdf_watcher.py: {e}")
else:
    print(f"❌ Fehler: {pdf_watcher_path} nicht gefunden!")

# Routen registrieren
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

@app.get("/")
def root():
    return {"message": "SCHUTZschild API läuft!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)