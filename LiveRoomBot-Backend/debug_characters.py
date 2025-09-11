#!/usr/bin/env python3
"""
Debug characters API
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.character_service import CharacterService
from app.schemas.character import Character
import json

def debug_characters():
    """Debug character retrieval"""
    
    print("🔍 Debugging character API...")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create character service
        char_service = CharacterService(db)
        
        # Get all active characters
        characters = char_service.get_all_active_characters()
        print(f"📊 Raw characters from service: {len(characters)}")
        
        for char in characters:
            print(f"  - Character: {char.name} (ID: {char.id})")
            print(f"    Display Name: {char.display_name}")
            print(f"    Active: {char.is_active}")
            print(f"    Avatar URLs: {char.avatar_urls}")
            print(f"    Traits: {char.traits}")
            
            # Try to serialize to schema
            try:
                char_schema = Character.model_validate(char)
                print(f"    ✅ Schema validation successful")
                print(f"    Schema dict: {char_schema.model_dump()}")
            except Exception as e:
                print(f"    ❌ Schema validation failed: {e}")
            
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_characters()
