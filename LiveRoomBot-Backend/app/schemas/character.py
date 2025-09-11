from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CharacterBase(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    personality: Optional[str] = None
    conversation_style: Optional[str] = None
    age_range: Optional[str] = None
    background_story: Optional[str] = None

class CharacterCreate(CharacterBase):
    category_id: int
    subcategory_id: Optional[int] = None
    system_prompt: Optional[str] = None
    avatar_urls: Optional[List[str]] = None
    traits: Optional[Dict[str, Any]] = None

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[str] = None
    system_prompt: Optional[str] = None
    avatar_urls: Optional[List[str]] = None
    traits: Optional[Dict[str, Any]] = None
    conversation_style: Optional[str] = None
    age_range: Optional[str] = None
    background_story: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None

class Character(CharacterBase):
    id: int
    avatar_urls: Optional[List[str]] = None
    traits: Optional[Dict[str, Any]] = None
    is_active: bool
    category_id: int
    subcategory_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class CharacterDetail(Character):
    system_prompt: Optional[str] = None
    
    class Config:
        from_attributes = True
