import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
print(f"🔍 SECRET_KEY: {SECRET_KEY}")  # Sollte NICHT None sein!
