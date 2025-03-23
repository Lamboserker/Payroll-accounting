from fastapi import FastAPI
from routes import auth, pdf, protected
import uvicorn
import subprocess
import os

app = FastAPI()

# Absoluten Pfad zur Datei ermitteln
server_path = os.path.dirname(os.path.abspath(__file__))  
pdf_watcher_path = os.path.join(server_path, "pdf_watcher.py")

if os.path.exists(pdf_watcher_path):
    subprocess.Popen([r"C:\Users\lukas\OneDrive\Desktop\SCHUTZschild payrollAccounting\Payroll-accounting\server\venv\Scripts\python.exe", pdf_watcher_path], cwd=server_path)
    print(f"✅ PDF-Watcher gestartet: {pdf_watcher_path}")
else:
    print(f"❌ Fehler: Datei {pdf_watcher_path} nicht gefunden!")

# Routen registrieren
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

@app.get("/")
def root():
    return {"message": "SCHUTZschild API läuft!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)