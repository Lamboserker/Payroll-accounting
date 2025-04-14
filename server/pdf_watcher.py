# from fastapi import APIRouter
# import os
# import shutil
# import time
# import threading
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from pymongo import MongoClient
# from datetime import datetime
# from bson import ObjectId
# import logging

# router = APIRouter()

# # Logger konfigurieren
# logger = logging.getLogger("pdf_watcher")
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("pdf_watcher_debug.log")
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# # MongoDB-Verbindung
# client = MongoClient("mongodb://localhost:27017")
# db = client["schutzzschild"]
# pdf_collection = db["pdf_documents"]
# user_collection = db["users"]

# # Basis-URL für den Download-Link
# BASE_DOWNLOAD_URL = "http://localhost:8000/static/pdfs/"

# # Flag, um den Watcher-Status zu verfolgen (Verhindern doppelte Ausführungen)
# watcher_thread = None
# watcher_running = False
# class PdfEventHandler(FileSystemEventHandler):
#     """Handler für Dateiereignisse im PDF-Überwachungsordner."""

#     def on_created(self, event):
#         """Wird ausgelöst, wenn eine neue Datei erstellt wird."""
#         if event.is_directory:
#             return
#         if event.src_path.endswith(".pdf"):
#             logger.info(f"PDF-Datei erkannt: {event.src_path}")
#             file_name = os.path.basename(event.src_path)
#             logger.info(f"Neue PDF-Datei erkannt: {file_name}")

#             try:
#                 # PDF-Verarbeitung
#                 creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 document_type = "Gehaltsabrechnung"
#                 destination_path = os.path.join("static", "pdfs", file_name)
#                 shutil.move(event.src_path, destination_path)
#                 download_link = BASE_DOWNLOAD_URL + file_name

#                 # Name extrahieren
#                 full_name = self.extract_name_from_filename(file_name)

#                 # Nutzer finden oder erstellen
#                 user_id = self.get_or_create_user(full_name)

#                 # PDF-Dokument in MongoDB speichern
#                 pdf_document = {
#                     "name": file_name,
#                     "creation_date": creation_date,
#                     "document_type": document_type,
#                     "download_link": download_link,
#                     "assigned_to": user_id
#                 }

#                 result = pdf_collection.insert_one(pdf_document)
#                 document_id = result.inserted_id
#                 logger.info(f"PDF-Datei in MongoDB gespeichert: {file_name}")

#                 # PDF-Dokument dem Nutzer zuordnen
#                 user_collection.update_one(
#                     {"_id": ObjectId(user_id)},
#                     {"$push": {"documents": document_id}}
#                 )
#                 logger.info(f"PDF '{file_name}' erfolgreich Benutzer '{full_name}' zugewiesen.")

#             except Exception as e:
#                 logger.exception(f"Fehler beim Verarbeiten der PDF-Datei: {file_name}")
#         else:
#             logger.debug(f"Es wurde keine PDF-Datei erkannt: {event.src_path}")

#     def extract_name_from_filename(self, file_name: str) -> str:
#         """Extrahiert den Namen des Mitarbeiters aus dem Dateinamen."""
#         name_parts = file_name.split("_")[:2]
#         full_name = " ".join(name_parts).strip()
#         return full_name

#     def get_or_create_user(self, full_name: str) -> str:
#         """Sucht einen Nutzer mit dem gegebenen Namen oder erstellt einen neuen."""
#         user = user_collection.find_one({"full_name": full_name})

#         if user:
#             logger.info(f"Nutzer '{full_name}' gefunden.")
#             return user["_id"]
#         else:
#             # Nutzer anlegen
#             new_user = {
#                 "full_name": full_name,
#                 "password": "1234",  # ⚠️ In Produktionsumgebung bitte hashen!
#                 "documents": []
#             }
#             user_id = user_collection.insert_one(new_user).inserted_id
#             logger.info(f"Neuer Nutzer '{full_name}' erstellt.")
#             return user_id


#     def extract_name_from_filename(self, file_name: str) -> str:
#         """Extrahiert den Namen des Mitarbeiters aus dem Dateinamen."""
#         name_parts = file_name.split("_")[:2]
#         full_name = " ".join(name_parts).strip()
#         return full_name

#     def get_or_create_user(self, full_name: str) -> str:
#         """Sucht einen Nutzer mit dem gegebenen Namen oder erstellt einen neuen."""
#         user = user_collection.find_one({"full_name": full_name})

#         if user:
#             logger.info(f"Nutzer '{full_name}' gefunden.")
#             return user["_id"]
#         else:
#             # Nutzer anlegen
#             new_user = {
#                 "full_name": full_name,
#                 "password": "1234",  # ⚠️ In Produktionsumgebung bitte hashen!
#                 "documents": []
#             }
#             user_id = user_collection.insert_one(new_user).inserted_id
#             logger.info(f"Neuer Nutzer '{full_name}' erstellt.")
#             return user_id
# def start_pdf_watcher(pdf_folder_path: str):
#     """Startet den PDF-Überwacher im angegebenen Ordner."""
#     global watcher_running
#     if watcher_running:
#         logger.warning("PDF-Watcher läuft bereits!")
#         return  # Verhindert doppelte Ausführung

#     watcher_running = True
#     event_handler = PdfEventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, pdf_folder_path, recursive=False)
#     observer.start()
#     logger.info(f"PDF-Watcher läuft in {pdf_folder_path}...")

#     try:
#         while watcher_running:
#             time.sleep(1)
#         logger.debug("Watcher beendet.")
#     except KeyboardInterrupt:
#         observer.stop()
#         logger.debug("Watcher gestoppt.")
#     observer.join()
#     watcher_running = False
#     logger.info("PDF-Watcher beendet.")

# # FastAPI-Router für den Start des Watchers
# @router.get("/start_pdf_watcher")
# def start_watcher(pdf_folder: str = r"C:\Users\SCHUTZschild\Desktop\PayrollSCHUTZschild\server\eingehende_pdfs"):
#     """Startet den PDF-Watcher über die API."""
#     # Überprüfen, ob der Ordner existiert
#     if not os.path.isdir(pdf_folder):
#         logger.error(f"Ordner {pdf_folder} existiert nicht oder ist ungültig.")
#         return {"error": "Der angegebene Ordner existiert nicht."}

#     # Starte den PDF-Watcher in einem neuen Thread, um die API nicht zu blockieren
#     global watcher_thread
#     if watcher_thread is None or not watcher_thread.is_alive():
#         watcher_thread = threading.Thread(target=start_pdf_watcher, args=(pdf_folder,))
#         watcher_thread.daemon = True  # Der Thread wird beendet, wenn die Hauptanwendung beendet wird
#         watcher_thread.start()
#         return {"message": "PDF-Watcher wurde gestartet."}
#     else:
#         return {"error": "PDF-Watcher läuft bereits."}


import os
import time
from pathlib import Path
from bson import ObjectId
from pymongo import MongoClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from models import User

# MongoDB-Verbindung
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.get_database()
user_collection = db["users"]

class PDFHandler(FileSystemEventHandler):
    """Handler, der auf Änderungen im PDF-Ordner reagiert"""
    
    def on_created(self, event):
        """Wenn eine neue Datei im Ordner hinzugefügt wird"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.pdf'):
            # Extrahiere den Dateinamen und bestimme den Benutzer
            filename = Path(event.src_path).name
            user_email = self.extract_user_from_filename(filename)
            if user_email:
                self.assign_pdf_to_user(event.src_path, user_email)
            else:
                print(f"Keine Benutzerzuordnung für Datei: {filename}")
    
    def extract_user_from_filename(self, filename):
        """Extrahiert die Benutzer-E-Mail aus dem Dateinamen"""
        # Beispiel: Angenommen, der Dateiname ist in folgendem Format: 'user_email_gehaltsabrechnung_01.pdf'
        parts = filename.split('_')
        if len(parts) > 1:
            return parts[0]  # Benutzer-E-Mail ist der erste Teil des Dateinamens
        return None
    
    def assign_pdf_to_user(self, pdf_path, user_email):
        """Weist die PDF dem richtigen Benutzer zu"""
        user = user_collection.find_one({"email": user_email})
        if user:
            user_folder = os.path.join('user_pdfs', user_email)
            os.makedirs(user_folder, exist_ok=True)
            new_pdf_path = os.path.join(user_folder, os.path.basename(pdf_path))
            os.rename(pdf_path, new_pdf_path)
            print(f"PDF für Benutzer {user_email} gespeichert unter {new_pdf_path}")
        else:
            print(f"Benutzer mit E-Mail {user_email} nicht gefunden!")

def start_pdf_watcher():
    """Startet den Watcher für den Ordner 'eingehende_pdfs'"""
    pdf_folder = 'eingehende_pdfs'
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, pdf_folder, recursive=False)
    observer.start()
    
    print(f"PDF Watcher läuft und überwacht den Ordner {pdf_folder}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("PDF Watcher gestoppt.")
    observer.join()

if __name__ == "__main__":
    start_pdf_watcher()
