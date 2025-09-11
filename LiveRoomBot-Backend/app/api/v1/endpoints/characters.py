from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.character import Character as CharacterModel
from app.schemas.character import Character, CharacterCreate, CharacterDetail
from app.services.character_service import CharacterService

router = APIRouter()

@router.get("/", response_model=List[Character])
def get_characters(
    category_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all characters, optionally filtered by category"""
    character_service = CharacterService(db)

    if category_id:
        characters = character_service.get_characters_by_category(category_id)
    else:
        characters = character_service.get_all_active_characters()

    return characters

@router.get("/{character_id}", response_model=CharacterDetail)
def get_character(character_id: int, db: Session = Depends(get_db)):
    """Get a specific character with full details"""
    character_service = CharacterService(db)
    character = character_service.get_character_by_id(character_id)
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return character

@router.post("/", response_model=Character)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    """Create a new character"""
    db_character = CharacterModel(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@router.get("/category/{category_id}", response_model=List[Character])
def get_characters_by_category(category_id: int, db: Session = Depends(get_db)):
    """Get all characters in a specific category"""
    character_service = CharacterService(db)
    characters = character_service.get_characters_by_category(category_id)
    return characters

@router.post("/from-persona/{persona_key}", response_model=Character)
def create_character_from_persona(
    persona_key: str, 
    category_id: int,
    db: Session = Depends(get_db)
):
    """Create a character from a predefined persona"""
    character_service = CharacterService(db)
    
    try:
        character = character_service.create_character_from_persona(persona_key, category_id)
        return character
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
