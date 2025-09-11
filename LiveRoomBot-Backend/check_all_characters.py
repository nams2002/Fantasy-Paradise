#!/usr/bin/env python3
"""
Check all characters and categories
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.character import Character
from app.models.category import Category

def check_all_characters():
    """Check all characters and categories"""
    
    print("🔍 Checking all characters and categories...")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Check categories
        categories = db.query(Category).all()
        print(f"📊 Total categories: {len(categories)}")
        
        for cat in categories:
            print(f"  - {cat.name} (ID: {cat.id})")
        
        # Check all characters
        all_characters = db.query(Character).all()
        print(f"\n📊 Total characters: {len(all_characters)}")
        
        # Check active characters
        active_characters = db.query(Character).filter(Character.is_active == True).all()
        print(f"📊 Active characters: {len(active_characters)}")
        
        # Group by category
        print(f"\n📋 Characters by category:")
        for cat in categories:
            cat_characters = db.query(Character).filter(Character.category_id == cat.id).all()
            active_cat_characters = db.query(Character).filter(
                Character.category_id == cat.id, 
                Character.is_active == True
            ).all()
            print(f"  {cat.name}: {len(cat_characters)} total, {len(active_cat_characters)} active")
            
            for char in cat_characters[:3]:  # Show first 3
                print(f"    - {char.display_name} (Active: {char.is_active})")
            if len(cat_characters) > 3:
                print(f"    ... and {len(cat_characters) - 3} more")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_all_characters()
