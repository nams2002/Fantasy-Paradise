from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.category import Category as CategoryModel
from app.schemas.category import Category, CategoryCreate, CategoryWithCharacters
from app.services.character_service import CharacterService

router = APIRouter()

@router.get("/", response_model=List[Category])
def get_categories(
    category_type: str = None,
    db: Session = Depends(get_db)
):
    """Get all categories, optionally filtered by type"""
    query = db.query(CategoryModel).filter(CategoryModel.is_active == True)
    
    if category_type:
        query = query.filter(CategoryModel.category_type == category_type)
    
    categories = query.order_by(CategoryModel.sort_order, CategoryModel.name).all()
    return categories

@router.get("/{category_id}", response_model=CategoryWithCharacters)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category with its characters"""
    category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id,
        CategoryModel.is_active == True
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/type/{category_type}", response_model=List[Category])
def get_categories_by_type(category_type: str, db: Session = Depends(get_db)):
    """Get categories by type (general, trending, latest)"""
    categories = db.query(CategoryModel).filter(
        CategoryModel.category_type == category_type,
        CategoryModel.is_active == True
    ).order_by(CategoryModel.sort_order, CategoryModel.name).all()
    
    return categories
