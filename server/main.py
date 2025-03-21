from fastapi import FastAPI
from routes import auth, pdf,protected
import uvicorn

app = FastAPI()

#Routen registrieren
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

@app.get("/")
def root():
    return {"message": "SCHUTZschild API läuft!"}

if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=8000)