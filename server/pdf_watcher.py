import os
import time
import fitz  # PyMuPDF für Textextraktion
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import spacy
import joblib  # Modell speichern und laden
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Ordnerpfade
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WATCH_FOLDER = os.path.join(BASE_DIR, "eingehende_pdfs")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "verarbeitete_pdfs")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# NLP-Modell laden (spaCy für Named Entity Recognition)
nlp = spacy.load("de_core_news_md")

# Modell für Dokumentklassifikation laden oder erstellen
MODEL_PATH = os.path.join(BASE_DIR, "document_classifier.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

def train_or_load_model():
    """Lädt oder trainiert ein verbessertes Naive Bayes Modell zur Dokumentklassifikation."""
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
    else:
        print("⚠ Kein Modell gefunden, Training mit Beispieldaten!")

        example_texts = {
            "Gehaltsabrechnung": [
                "Gehaltsabrechnung Mai 2023 - Brutto: 2500€, Netto: 1800€, Steuerklasse 1",
                "Gehaltsabrechnung Juni 2023 - Abzüge: Sozialversicherung, Rentenversicherung",
                "Abrechnung der Brutto/Netto-Bezüge - Lohnabrechnung für Max Mustermann"
            ],
            "Arbeitsvertrag": [
                "Arbeitsvertrag - Angestellt als Softwareentwickler bei Müller GmbH",
                "Arbeitsvertrag - Befristet für 12 Monate, unterschrieben am 10.01.2023"
            ],
            "Kündigung": [
                "Kündigungsschreiben - Fristlose Kündigung durch Arbeitgeber, Paragraph XY",
                "Kündigung - Vertrag endet zum 31.12.2023 wegen betrieblicher Umstrukturierung"
            ]
        }

        # ✅ Liste erstellen für Trainingsdaten & Labels
        example_text_list = []
        labels = []
        for category, texts in example_texts.items():
            example_text_list.extend(texts)
            labels.extend([category] * len(texts))

        # ✅ Vektorizer und Modell korrekt initialisieren
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(example_text_list)  # Korrektur!
        model = MultinomialNB()
        model.fit(X, labels)

        # ✅ Trainiertes Modell speichern
        joblib.dump(model, MODEL_PATH)
        joblib.dump(vectorizer, VECTORIZER_PATH)

    return model, vectorizer


model, vectorizer = train_or_load_model()

def extract_text_from_pdf(pdf_path):
    """Extrahiert den gesamten Text aus einer PDF-Datei."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def classify_document(text):
    """Klassifiziert das Dokument basierend auf ML, aber prüft Gehaltsabrechnungen separat."""
    if any(keyword in text.lower() for keyword in ["brutto", "netto", "lohnabrechnung", "steuerklasse"]):
        return "Zuk.sich_Gehaltsabrechnung"
    
    X_new = vectorizer.transform([text])
    prediction = model.predict(X_new)[0]
    return prediction

def detect_document_type_and_employee(text):
    """Erkennt den Dokumenttyp und den Namen des Mitarbeiters."""
    doc_type = classify_document(text)
    employee_name = "Unbekannt"
    
    # Mitarbeitername erkennen
    doc_nlp = nlp(text)
    for ent in doc_nlp.ents:
        if ent.label_ == "PER":
            employee_name = ent.text
            break
    
    # Falls kein Name gefunden wurde, mit Regex nach "Herr/Frau [Nachname]" suchen
    if employee_name == "Unbekannt":
        match = re.search(r"(Herr|Frau) (\w+)", text)
        if match:
            employee_name = match.group(2)  # Nachname extrahieren
    
    return sanitize_filename(doc_type), sanitize_filename(employee_name)

def sanitize_filename(filename):
    """Entfernt unerlaubte Zeichen aus Dateinamen"""
    return re.sub(r'[<>:"/\\|?*\n]', '_', filename)

def rename_pdf(file_path):
    """Bestimmt den neuen Dateinamen basierend auf dem Inhalt."""
    text = extract_text_from_pdf(file_path)
    doc_type, employee_name = detect_document_type_and_employee(text)
    
    new_filename = f"{employee_name}_{doc_type}.pdf"
    new_path = os.path.join(PROCESSED_FOLDER, new_filename)
    
    # Falls Datei bereits existiert, eine Nummerierung hinzufügen
    base, ext = os.path.splitext(new_filename)
    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{base}({counter}){ext}"
        new_path = os.path.join(PROCESSED_FOLDER, new_filename)
        counter += 1
    
    shutil.move(file_path, new_path)
    print(f"✅ Datei umbenannt: {new_filename}")

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            time.sleep(2)  # Warten, um sicherzustellen, dass die Datei vollständig geschrieben ist
            rename_pdf(event.src_path)

if __name__ == "__main__":
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    print(f"👀 Überwache Ordner: {WATCH_FOLDER}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()