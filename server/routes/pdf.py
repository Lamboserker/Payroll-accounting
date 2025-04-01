from fastapi import APIRouter
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

router = APIRouter()

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
            print(f"Neue PDF-Datei erkannt: {file_name}")
            try:
                result = assign_pdf_to_user(file_name)
                print(result["message"])
            except Exception as e:
                print(f"Fehler beim Zuweisen der PDF-Datei: {e}")

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
