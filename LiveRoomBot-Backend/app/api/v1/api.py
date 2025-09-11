from fastapi import APIRouter
from app.api.v1.endpoints import categories, characters, chat, community
from app.api.v1 import subcategories

api_router = APIRouter()

api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(subcategories.router, prefix="/subcategories", tags=["subcategories"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(community.router, prefix="/community", tags=["community"])
