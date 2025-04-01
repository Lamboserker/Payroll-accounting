from fastapi import APIRouter, Depends, HTTPException
from routes.auth import get_current_user

router = APIRouter()

def check_role(user, required_role):
    if user["role"] not in required_role:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")

@router.get("/admin")
def admin_dashboard(user: dict = Depends(get_current_user)):
    check_role(user, ["admin", "root"])
    return {"message": "Admin-Dashboard", "user": user["email"]}

@router.get("/root")
def root_dashboard(user: dict = Depends(get_current_user)):
    check_role(user, ["root"])
    return {"message": "Root-Dashboard", "user": user["email"]}