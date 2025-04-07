from fastapi import APIRouter, Depends
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import threading
from pymongo import MongoClient

router = APIRouter()

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Ersetze durch deine Verbindung

db = client.schutzschild_db
pdf_collection = db.lohnabrechnungen


document_queue = []  # Warteschlange für erkannte PDFs
watcher_running = False
observer = None

def extract_user_from_filename(file_name):
    """ Extrahiert den Nutzer aus dem Dateinamen: Beispiel 'Mia_Lange_Lohnabrechnung_Februar_2022.pdf' """
    parts = file_name.split("_")
    if len(parts) >= 2:
        return f"{parts[0]} {parts[1]}"  # Vorname + Nachname
    return None

def save_pdf_to_db(file_name):
    """ Speichert die Lohnabrechnung in MongoDB und weist sie dem Nutzer zu """
    user_name = extract_user_from_filename(file_name)
    if not user_name:
        print(f"⚠️ Konnte Nutzer aus Dateinamen nicht extrahieren: {file_name}")
        return
    
    pdf_entry = {
        "user": user_name,
        "file_name": file_name,
        "status": "pending"  # Nutzer sieht sie, kann sie aber erst per Klick laden
    }
    pdf_collection.insert_one(pdf_entry)
    print(f"✅ Lohnabrechnung gespeichert für {user_name}: {file_name}")

class PdfEventHandler(FileSystemEventHandler):
    """ Handler für Datei-Ereignisse """
    
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            file_name = os.path.basename(event.src_path)
            print(f"📂 Neue PDF erkannt: {file_name}")
            document_queue.append(file_name)
            save_pdf_to_db(file_name)

def start_pdf_watcher(pdf_folder_path: str):
    global observer, watcher_running
    if watcher_running:
        return {"message": "PDF-Watcher läuft bereits."}
    
    event_handler = PdfEventHandler()
    observer = Observer()
    observer.schedule(event_handler, pdf_folder_path, recursive=False)
    
    def run():
        global watcher_running
        observer.start()
        watcher_running = True
        print(f"👀 PDF-Watcher läuft in {pdf_folder_path}...")
        try:
            while watcher_running:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        watcher_running = False
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return {"message": f"PDF-Watcher gestartet in {pdf_folder_path}"}

@router.get("/admin/start_pdf_watcher")
def start_watcher(pdf_folder: str = "server/eingehende_pdfs"):
    return start_pdf_watcher(pdf_folder)
