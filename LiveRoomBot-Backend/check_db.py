#!/usr/bin/env python3
"""
Check database contents
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine
from app.models.character import Character
from app.models.category import Category
from app.core.database import get_db

def check_database():
    """Check what's in the database"""
    
    print("🔍 Checking database contents...")
    
    try:
        # Check characters count
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM characters"))
            char_count = result.scalar()
            print(f"📊 Characters in database: {char_count}")
            
            # Check categories count
            result = conn.execute(text("SELECT COUNT(*) FROM categories"))
            cat_count = result.scalar()
            print(f"📊 Categories in database: {cat_count}")
            
            # List all characters
            if char_count > 0:
                result = conn.execute(text("SELECT id, name, display_name FROM characters"))
                characters = result.fetchall()
                print("\n📋 Characters found:")
                for char in characters:
                    print(f"  - ID: {char[0]}, Name: {char[1]}, Display: {char[2]}")
            
            # List all categories
            if cat_count > 0:
                result = conn.execute(text("SELECT id, name, description FROM categories"))
                categories = result.fetchall()
                print("\n📋 Categories found:")
                for cat in categories:
                    print(f"  - ID: {cat[0]}, Name: {cat[1]}, Description: {cat[2]}")
                    
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_database()
