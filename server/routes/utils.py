from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# MongoDB-Verbindung
client = MongoClient('mongodb://localhost:27017/')
db = client['pdf_database']
user_collection = db['users']
pdf_collection = db['pdf_documents']

BASE_DOWNLOAD_URL = "http://localhost:5000/static/pdfs/"

class PdfEventHandler(FileSystemEventHandler):
    """Handler für Dateiereignisse im PDF-Überwachungsordner."""

    def on_created(self, event):
        # Wenn es sich um ein Verzeichnis handelt, ignorieren wir es
        if event.is_directory or not event.src_path.endswith(".pdf"):
            return

        file_name = os.path.basename(event.src_path)
        print(f"Neue PDF-Datei erkannt: {file_name}")

        try:
            # 1. Basisdaten
            creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            document_type = "Gehaltsabrechnung"
            destination_path = os.path.join("static", "pdfs", file_name)
            shutil.move(event.src_path, destination_path)
            download_link = BASE_DOWNLOAD_URL + file_name

            # 2. Extrahiere Namen aus Dateinamen (z. B. Max_Mustermann_März_2025.pdf)
            name_parts = file_name.split("_")[:2]
            full_name = " ".join(name_parts).strip()

            # 3. Suche Nutzer mit diesem Namen
            user = user_collection.find_one({"full_name": full_name})

            if user:
                user_id = user["_id"]
                print(f"Nutzer '{full_name}' gefunden.")
            else:
                # 4. Nutzer existiert nicht – neu anlegen
                new_user = {
                    "full_name": full_name,
                    "password": "1234",  # ⚠ In Produktivumgebung bitte unbedingt hashen!
                    "documents": []
                }
                user_id = user_collection.insert_one(new_user).inserted_id
                print(f"Neuer Nutzer '{full_name}' erstellt mit Standardpasswort.")

            # 5. Speichere PDF-Dokument
            pdf_document = {
                "name": file_name,
                "creation_date": creation_date,
                "document_type": document_type,
                "download_link": download_link,
                "assigned_to": user_id
            }

            result = pdf_collection.insert_one(pdf_document)
            document_id = result.inserted_id
            print(f"PDF-Datei in MongoDB gespeichert: {file_name}")

            # 6. PDF-Dokument dem Nutzer zuordnen
            user_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"documents": document_id}}
            )
            print(f"PDF '{file_name}' erfolgreich Benutzer '{full_name}' zugewiesen.")

        except Exception as e:
            print(f"Fehler beim Verarbeiten der PDF-Datei: {e}")


def start_pdf_watcher():
    # Pfad zum Ordner, der überwacht werden soll
    pdf_folder = 'eingehende_pdfs'  # Den genauen Ordnernamen anpassen

    event_handler = PdfEventHandler()
    observer = Observer()
    observer.schedule(event_handler, pdf_folder, recursive=False)  # Keine rekursive Überwachung
    observer.start()

    print(f"Überwachung des Ordners '{pdf_folder}' gestartet.")

    try:
        while True:
            # Endlosschleife für den Observer
            pass
    except KeyboardInterrupt:
        observer.stop()
        print("Beendet!")
    observer.join()

if __name__ == "__main__":
    start_pdf_watcher()
