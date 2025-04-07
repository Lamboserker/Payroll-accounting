from fastapi import APIRouter
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from pymongo import MongoClient
from datetime import datetime
import shutil

router = APIRouter()

# MongoDB-Verbindung
client = MongoClient("mongodb://localhost:27017")  # Stelle sicher, dass die Verbindung zur richtigen MongoDB-Instanz erfolgt
db = client["schutzzschild"]  # Deine MongoDB-Datenbank
pdf_collection = db["pdf_documents"]  # Die Sammlung für die gespeicherten PDFs

# Basis-URL für den Download-Link (dieser muss angepasst werden, je nachdem, wie die Dateien zugänglich sind)
BASE_DOWNLOAD_URL = "http://localhost:8000/static/pdfs/"

# Test-Route, um zu überprüfen, ob der PDF-Endpoint funktioniert
@router.get("/test")
def test_pdf():
    return {"message": "PDF-Endpoint funktioniert"}

class PdfEventHandler(FileSystemEventHandler):
    """Handler für Dateiereignisse im PDF-Überwachungsordner."""
    
    def on_created(self, event):
        """Wird ausgelöst, wenn eine neue Datei erstellt wird."""
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            file_name = os.path.basename(event.src_path)
            file_path = event.src_path
            print(f"Neue PDF-Datei erkannt: {file_name}")

            try:
                # Dateimetadaten speichern
                creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                document_type = "Gehaltsabrechnung"  # Dies kann weiter angepasst werden, je nachdem, wie du das Dokument kategorisieren möchtest
                
                # Verschiebe die Datei in den statischen Ordner für den Download
                destination_path = os.path.join("static", "pdfs", file_name)
                shutil.move(file_path, destination_path)

                # Generiere den Download-Link
                download_link = BASE_DOWNLOAD_URL + file_name

                # Speichere die Metadaten in MongoDB
                pdf_document = {
                    "name": file_name,
                    "creation_date": creation_date,
                    "document_type": document_type,
                    "download_link": download_link
                }

                pdf_collection.insert_one(pdf_document)
                print(f"PDF-Datei in MongoDB gespeichert: {file_name}")

            except Exception as e:
                print(f"Fehler beim Verarbeiten der PDF-Datei: {e}")

def start_pdf_watcher(pdf_folder_path: str):
    """Startet den PDF-Überwacher im angegebenen Ordner."""
    event_handler = PdfEventHandler()
    observer = Observer()
    observer.schedule(event_handler, pdf_folder_path, recursive=False)
    observer.start()
    print(f"PDF-Watcher läuft in {pdf_folder_path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Neue Route, um den PDF-Watcher zu starten
@router.get("/start_pdf_watcher")
def start_watcher(pdf_folder: str = "server\\eingehende_pdfs"):
    """Startet den PDF-Watcher über die API."""
    try:
        start_pdf_watcher(pdf_folder)
        return {"message": f"PDF-Watcher gestartet in {pdf_folder}"}
    except Exception as e:
        return {"message": f"Fehler beim Starten des Watchers: {e}"}
