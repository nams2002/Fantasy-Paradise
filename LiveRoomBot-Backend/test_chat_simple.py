#!/usr/bin/env python3
import requests
import json

# First, get the characters to find Luna's ID
try:
    response = requests.get('http://localhost:8000/api/v1/characters/')
    if response.status_code == 200:
        characters = response.json()
        print(f'Found {len(characters)} characters')

        # Find Luna
        luna = None
        for char in characters:
            if 'Luna' in char['display_name'] and 'Flirty' in char['display_name']:
                luna = char
                break

        if luna:
            print(f'Found Luna: ID {luna["id"]}, Name: {luna["display_name"]}')

            # Test chat with Luna
            chat_data = {
                'message': 'Hello Luna! How are you today?',
                'character_id': luna['id'],
                'user_id': 1
            }

            response = requests.post('http://localhost:8000/api/v1/chat/send',
                                   json=chat_data,
                                   headers={'Content-Type': 'application/json'})
            print(f'Chat Status: {response.status_code}')
            if response.status_code == 200:
                result = response.json()
                print(f'✅ Chat successful!')
                print(f'Character: {result.get("character_name", "Unknown")}')
                print(f'Response: {result.get("response", "No response")}')
            else:
                print(f'❌ Chat Error: {response.status_code}')
                print(f'Response: {response.text}')
        else:
            print('❌ Luna not found')
    else:
        print(f'❌ Characters API Error: {response.status_code}')

except Exception as e:
    print(f'❌ Request failed: {e}')
