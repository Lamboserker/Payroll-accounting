from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Lade die .env-Datei
load_dotenv()

# Debugging: Prüfen, ob Werte aus .env geladen werden
print("🔍 DEBUG: MONGO_URI =", os.getenv("MONGO_URI"))

uri= os.getenv("MONGO_URI")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.schutzschild_db
#pdf_collection = db["lohnabrechnungen"]

if not client:
    raise ValueError("❌ MONGO_URI ist nicht gesetzt! Prüfe deine .env Datei.")
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#try:
#    client = MongoClient(MONGO_URI, server_api=ServerApi('1'), connectTimeoutMS=30000, socketTimeoutMS=30000)
#    db = client["schutzschild_db"]
#    client.admin.command("ping")
#    print("✅ Verbindung erfolgreich zu MongoDB Atlas!")
#except Exception as e:
#    print(f"❌ Fehler bei MongoDB-Verbindung: {e}")
#    print(f"🔍 Details: {str(e)}")




# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# import os
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")

# if not MONGO_URI:
#     raise ValueError("❌ MONGO_URI ist nicht gesetzt! Prüfe deine .env Datei.")

# try:
#     client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
#     db = client["schutzschild_db"]
#     client.admin.command("ping")
#     print("✅ Verbindung erfolgreich zu MongoDB Atlas!")
# except Exception as e:
#     print(f"❌ Fehler bei MongoDB-Verbindung: {e}")