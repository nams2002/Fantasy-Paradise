#!/usr/bin/env python3
import sys
sys.path.append('.')
from app.services.character_service import CharacterPersonas

all_personas = CharacterPersonas.get_all_personas()
print('Available personas:')
for key in sorted(all_personas.keys()):
    persona = all_personas[key]
    category = persona.get('category', 'unknown')
    print(f'  {key}: {persona["display_name"]} ({category})')

print(f'\nTotal personas: {len(all_personas)}')

# Count by category
categories = {}
for persona in all_personas.values():
    cat = persona.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1

print('\nBy category:')
for cat, count in sorted(categories.items()):
    print(f'  {cat}: {count}')
