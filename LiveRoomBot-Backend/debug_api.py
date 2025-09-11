#!/usr/bin/env python3
"""
Debug API endpoint directly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.character_service import CharacterService
from app.schemas.character import Character
from typing import List

def debug_api_endpoint():
    """Debug the exact API endpoint logic"""
    
    print("🔍 Debugging API endpoint logic...")
    
    try:
        # Simulate the exact API endpoint logic
        db = next(get_db())
        character_service = CharacterService(db)
        
        # Get characters (same as API)
        characters = character_service.get_all_active_characters()
        print(f"📊 Characters from service: {len(characters)}")
        
        # Convert to response model (same as FastAPI does)
        response_data = []
        for char in characters:
            try:
                char_dict = Character.model_validate(char).model_dump()
                response_data.append(char_dict)
                print(f"  ✅ Converted: {char.name}")
            except Exception as e:
                print(f"  ❌ Failed to convert {char.name}: {e}")
        
        print(f"📋 Final response data length: {len(response_data)}")
        
        # Test JSON serialization
        import json
        try:
            json_str = json.dumps(response_data, indent=2)
            print(f"✅ JSON serialization successful")
            print(f"📄 First character preview:")
            if response_data:
                print(json.dumps(response_data[0], indent=2)[:500] + "...")
        except Exception as e:
            print(f"❌ JSON serialization failed: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_api_endpoint()
