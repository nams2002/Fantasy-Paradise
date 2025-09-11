from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.subcategory import Subcategory
from app.models.category import Category
from app.schemas.subcategory import SubcategoryResponse

router = APIRouter()

@router.get("/", response_model=List[SubcategoryResponse])
def get_subcategories(
    category_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all subcategories or subcategories for a specific category"""
    query = db.query(Subcategory).filter(Subcategory.is_active == True)
    
    if category_id:
        query = query.filter(Subcategory.category_id == category_id)
    
    subcategories = query.order_by(Subcategory.sort_order).all()
    return subcategories

@router.get("/{subcategory_id}", response_model=SubcategoryResponse)
def get_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    """Get a specific subcategory by ID"""
    subcategory = db.query(Subcategory).filter(
        Subcategory.id == subcategory_id,
        Subcategory.is_active == True
    ).first()
    
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    
    return subcategory

@router.get("/category/{category_id}", response_model=List[SubcategoryResponse])
def get_subcategories_by_category(category_id: int, db: Session = Depends(get_db)):
    """Get all subcategories for a specific category"""
    # Verify category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    subcategories = db.query(Subcategory).filter(
        Subcategory.category_id == category_id,
        Subcategory.is_active == True
    ).order_by(Subcategory.sort_order).all()
    
    return subcategories
