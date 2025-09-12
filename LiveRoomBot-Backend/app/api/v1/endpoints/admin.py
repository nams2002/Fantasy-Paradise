from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.scripts.init_data import init_database

router = APIRouter()

@router.post("/seed")
def seed_database(token: str):
    """Run one-time DB seeding (idempotent). Protect with a secret token."""
    expected = settings.SEED_SECRET or settings.SECRET_KEY
    if not token or token != expected:
        raise HTTPException(status_code=403, detail="Forbidden")
    init_database()
    return {"status": "ok", "message": "Seeding completed (idempotent)"}

