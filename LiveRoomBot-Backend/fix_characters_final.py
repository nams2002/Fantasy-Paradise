#!/usr/bin/env python3
"""
Fix characters with proper boolean values using SQLAlchemy
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.character import Character
from sqlalchemy.orm import Session

def fix_characters():
    """Fix characters with proper boolean values"""
    
    print("🔧 Fixing characters with SQLAlchemy...")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Get all characters
        characters = db.query(Character).all()
        print(f"📊 Found {len(characters)} characters")
        
        # Update each character to ensure proper boolean values
        for char in characters:
            print(f"  - Updating {char.name}: is_active = {char.is_active} (type: {type(char.is_active)})")
            char.is_active = True  # Set to proper Python boolean
            
        # Commit changes
        db.commit()
        print("✅ Updated all characters with proper boolean values")
        
        # Verify the fix
        active_characters = db.query(Character).filter(Character.is_active == True).all()
        print(f"📊 Active characters after fix: {len(active_characters)}")
        
        for char in active_characters:
            print(f"  - {char.display_name} (ID: {char.id})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    fix_characters()
