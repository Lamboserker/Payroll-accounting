from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_pdf():
    return {"message": "PDF-Endpoint funktioniert"}
