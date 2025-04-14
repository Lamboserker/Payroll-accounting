import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Ordner, den du überwachen willst
pdf_folder = r"C:\Users\SCHUTZschild\Desktop\PayrollSCHUTZschild\server\eingehende_pdfs"

class PdfEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            print(f"📂 Neue PDF erkannt: {os.path.basename(event.src_path)}")

def start_watcher():
    # Sicherstellen, dass der Ordner existiert
    if not os.path.exists(pdf_folder):
        print(f"❌ Ordner existiert nicht: {pdf_folder}")
        return
    
    print(f"🔍 Starte den PDF-Watcher für {pdf_folder}...")

    event_handler = PdfEventHandler()
    observer = Observer()
    observer.schedule(event_handler, pdf_folder, recursive=False)
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

start_watcher()
