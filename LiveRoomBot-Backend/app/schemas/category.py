from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_type: str = "general"
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class Category(CategoryBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class CategoryWithCharacters(Category):
    characters: List['Character'] = []
    
    class Config:
        from_attributes = True

# Import Character here to avoid circular imports
from app.schemas.character import Character
CategoryWithCharacters.model_rebuild()
