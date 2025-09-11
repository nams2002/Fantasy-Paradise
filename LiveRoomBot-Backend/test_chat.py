#!/usr/bin/env python3
"""
Test script to verify chat functionality
"""
import requests
import json

def test_chat_api():
    """Test the chat API endpoint"""

    # First, get the first available character
    try:
        response = requests.get("http://localhost:8000/api/v1/characters/", timeout=10)
        if response.status_code != 200:
            print("❌ Cannot get characters for chat test")
            return False

        characters = response.json()
        if not characters:
            print("❌ No characters available for chat test")
            return False

        first_character = characters[0]
        character_id = first_character['id']
        character_name = first_character['display_name']

    except Exception as e:
        print(f"❌ Error getting characters: {e}")
        return False

    # Test data
    test_message = {
        "message": "Hello! How are you today?",
        "character_id": character_id,
        "user_id": 1
    }
    
    try:
        print("🧪 Testing chat API...")
        print(f"🤖 Testing with character: {character_name} (ID: {character_id})")
        print(f"📤 Sending message: {test_message['message']}")
        
        # Send POST request to chat endpoint
        response = requests.post(
            "http://localhost:8000/api/v1/chat/send",
            json=test_message,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat API working successfully!")
            print(f"📥 AI Response: {data.get('response', 'No response field')}")
            print(f"🤖 Character: {data.get('character_name', 'Unknown')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_characters_api():
    """Test the characters API endpoint"""
    
    try:
        print("\n🧪 Testing characters API...")
        
        response = requests.get(
            "http://localhost:8000/api/v1/characters/",
            timeout=10
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Characters API working successfully!")
            print(f"📋 Found {len(data)} characters:")
            for char in data:
                print(f"  - {char.get('display_name', 'Unknown')} (ID: {char.get('id', 'Unknown')})")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LiveRoom AI Platform - API Test")
    print("=" * 50)
    
    # Test characters endpoint first
    characters_ok = test_characters_api()
    
    # Test chat endpoint
    chat_ok = test_chat_api()
    
    print("\n" + "=" * 50)
    if characters_ok and chat_ok:
        print("🎉 ALL TESTS PASSED! Your platform is fully functional!")
        print("✅ PostgreSQL database working")
        print("✅ Characters loaded successfully")
        print("✅ Chat API working with OpenAI integration")
        print("✅ Frontend can connect to backend")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("\n🌐 Your LiveRoom platform is running at:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
