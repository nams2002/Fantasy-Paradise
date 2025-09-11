import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.character import Character
from app.models.user import User
import json

class CharacterMoodService:
    """Service for managing dynamic character moods that affect behavior"""
    
    # Mood definitions with effects on conversation
    MOODS = {
        "happy": {
            "name": "Happy",
            "emoji": "😊",
            "description": "Cheerful and upbeat",
            "probability": 0.25,
            "effects": {
                "energy_level": 1.2,
                "flirtiness": 1.1,
                "positivity": 1.3,
                "playfulness": 1.2
            },
            "greeting_modifiers": [
                "I'm feeling absolutely wonderful today! ",
                "I'm in such a great mood! ",
                "Everything feels amazing right now! "
            ],
            "response_modifiers": [
                " *beaming with joy*",
                " *with a bright smile*",
                " *radiating happiness*"
            ]
        },
        "flirty": {
            "name": "Flirty",
            "emoji": "😘",
            "description": "Extra playful and seductive",
            "probability": 0.20,
            "effects": {
                "flirtiness": 1.5,
                "playfulness": 1.3,
                "seductiveness": 1.4,
                "confidence": 1.2
            },
            "greeting_modifiers": [
                "I'm feeling particularly... playful today~ ",
                "Someone's looking irresistible today... ",
                "I can't help but feel extra flirty around you~ "
            ],
            "response_modifiers": [
                " *with a mischievous wink*",
                " *biting lip playfully*",
                " *with a sultry smile*"
            ]
        },
        "mysterious": {
            "name": "Mysterious",
            "emoji": "🌙",
            "description": "Enigmatic and intriguing",
            "probability": 0.15,
            "effects": {
                "mystery": 1.4,
                "depth": 1.3,
                "intrigue": 1.5,
                "directness": 0.7
            },
            "greeting_modifiers": [
                "There's something different in the air today... ",
                "I have secrets I might share... if you're worthy. ",
                "The shadows whisper interesting things today... "
            ],
            "response_modifiers": [
                " *with an enigmatic smile*",
                " *eyes gleaming with secrets*",
                " *mysteriously*"
            ]
        },
        "romantic": {
            "name": "Romantic",
            "emoji": "💕",
            "description": "Extra loving and affectionate",
            "probability": 0.20,
            "effects": {
                "romance": 1.4,
                "affection": 1.5,
                "intimacy": 1.3,
                "sweetness": 1.4
            },
            "greeting_modifiers": [
                "My heart feels so full when I see you... ",
                "Love is in the air, can you feel it? ",
                "You make everything feel like a fairy tale... "
            ],
            "response_modifiers": [
                " *with loving eyes*",
                " *heart fluttering*",
                " *melting with affection*"
            ]
        },
        "energetic": {
            "name": "Energetic",
            "emoji": "⚡",
            "description": "Full of energy and excitement",
            "probability": 0.15,
            "effects": {
                "energy_level": 1.6,
                "enthusiasm": 1.5,
                "playfulness": 1.3,
                "spontaneity": 1.4
            },
            "greeting_modifiers": [
                "I'm bursting with energy today! ",
                "I feel like I could conquer the world! ",
                "So much excitement, I can barely contain it! "
            ],
            "response_modifiers": [
                " *bouncing with excitement*",
                " *practically vibrating with energy*",
                " *eyes sparkling with enthusiasm*"
            ]
        },
        "contemplative": {
            "name": "Contemplative",
            "emoji": "🤔",
            "description": "Thoughtful and philosophical",
            "probability": 0.10,
            "effects": {
                "depth": 1.5,
                "wisdom": 1.4,
                "introspection": 1.6,
                "playfulness": 0.8
            },
            "greeting_modifiers": [
                "I've been thinking deeply about life today... ",
                "There's so much beauty in quiet moments... ",
                "My mind is wandering to profound places... "
            ],
            "response_modifiers": [
                " *thoughtfully*",
                " *with deep consideration*",
                " *pondering the deeper meaning*"
            ]
        }
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_character_mood(self, character_id: int, user_id: int) -> Dict:
        """Get current mood for a character (user-specific)"""
        # In production, you might store this in a separate table
        # For now, we'll generate based on character and user interaction
        
        character = self.db.query(Character).filter(Character.id == character_id).first()
        if not character:
            return self._get_default_mood()
        
        # Generate mood based on character personality and time
        mood_key = self._determine_character_mood(character, user_id)
        mood = self.MOODS[mood_key].copy()
        mood["key"] = mood_key
        mood["duration_hours"] = random.randint(2, 8)  # Mood lasts 2-8 hours
        mood["started_at"] = datetime.utcnow()
        
        return mood
    
    def _determine_character_mood(self, character: Character, user_id: int) -> str:
        """Determine character's current mood based on personality and factors"""
        # Base mood probabilities
        mood_weights = {}
        
        for mood_key, mood_data in self.MOODS.items():
            base_probability = mood_data["probability"]
            
            # Adjust based on character traits
            if hasattr(character, 'traits') and character.traits:
                traits = character.traits if isinstance(character.traits, dict) else {}
                
                # Boost mood probability based on character traits
                if mood_key == "flirty" and traits.get("flirty", 0) > 7:
                    base_probability *= 1.5
                elif mood_key == "romantic" and traits.get("romantic", 0) > 7:
                    base_probability *= 1.5
                elif mood_key == "energetic" and traits.get("energetic", 0) > 7:
                    base_probability *= 1.5
                elif mood_key == "mysterious" and traits.get("mysterious", 0) > 7:
                    base_probability *= 1.5
            
            # Adjust based on conversation style
            if hasattr(character, 'conversation_style'):
                if character.conversation_style == "flirty" and mood_key == "flirty":
                    base_probability *= 1.3
                elif character.conversation_style == "romantic" and mood_key == "romantic":
                    base_probability *= 1.3
                elif character.conversation_style == "energetic" and mood_key == "energetic":
                    base_probability *= 1.3
            
            # Time-based adjustments (morning = energetic, evening = romantic, etc.)
            hour = datetime.utcnow().hour
            if mood_key == "energetic" and 6 <= hour <= 12:
                base_probability *= 1.2
            elif mood_key == "romantic" and (18 <= hour <= 23 or 0 <= hour <= 2):
                base_probability *= 1.2
            elif mood_key == "contemplative" and (22 <= hour <= 24 or 0 <= hour <= 6):
                base_probability *= 1.3
            
            mood_weights[mood_key] = base_probability
        
        # Weighted random selection
        return self._weighted_random_choice(mood_weights)
    
    def _weighted_random_choice(self, weights: Dict[str, float]) -> str:
        """Select a random choice based on weights"""
        total = sum(weights.values())
        r = random.uniform(0, total)
        
        cumulative = 0
        for choice, weight in weights.items():
            cumulative += weight
            if r <= cumulative:
                return choice
        
        return list(weights.keys())[0]  # Fallback
    
    def _get_default_mood(self) -> Dict:
        """Get default mood when character not found"""
        mood = self.MOODS["happy"].copy()
        mood["key"] = "happy"
        return mood
    
    def apply_mood_to_prompt(self, base_prompt: str, character_id: int, user_id: int) -> str:
        """Apply character's current mood to the system prompt"""
        mood = self.get_character_mood(character_id, user_id)
        
        mood_enhancement = f"""

CURRENT MOOD: {mood['name']} {mood['emoji']}
Mood Description: {mood['description']}

MOOD EFFECTS ON PERSONALITY:
"""
        
        for effect, multiplier in mood['effects'].items():
            if multiplier > 1.0:
                mood_enhancement += f"- {effect.replace('_', ' ').title()}: Enhanced ({multiplier}x)\n"
            elif multiplier < 1.0:
                mood_enhancement += f"- {effect.replace('_', ' ').title()}: Reduced ({multiplier}x)\n"
        
        mood_enhancement += f"""
MOOD-SPECIFIC INSTRUCTIONS:
- Start responses with one of these mood modifiers: {', '.join(mood['greeting_modifiers'])}
- End responses with mood actions: {', '.join(mood['response_modifiers'])}
- Adjust your personality traits according to the mood effects above
- Let this mood naturally influence your conversation style
- Be consistent with this mood throughout the conversation
"""
        
        return base_prompt + mood_enhancement
    
    def get_mood_status(self, character_id: int, user_id: int) -> Dict:
        """Get detailed mood status for frontend display"""
        mood = self.get_character_mood(character_id, user_id)
        
        return {
            "current_mood": {
                "name": mood["name"],
                "emoji": mood["emoji"],
                "description": mood["description"],
                "key": mood["key"]
            },
            "effects": mood["effects"],
            "duration_remaining": "2-8 hours",  # In production, calculate actual remaining time
            "next_mood_change": "In a few hours",
            "mood_history": self._get_recent_moods(character_id, user_id)
        }
    
    def _get_recent_moods(self, character_id: int, user_id: int) -> List[Dict]:
        """Get recent mood history (mock data for now)"""
        # In production, store and retrieve actual mood history
        recent_moods = [
            {"mood": "romantic", "emoji": "💕", "time": "2 hours ago"},
            {"mood": "happy", "emoji": "😊", "time": "6 hours ago"},
            {"mood": "flirty", "emoji": "😘", "time": "1 day ago"}
        ]
        return recent_moods
    
    def trigger_mood_change(self, character_id: int, user_id: int, new_mood: str = None) -> Dict:
        """Manually trigger a mood change (for special events or admin)"""
        if new_mood and new_mood not in self.MOODS:
            raise ValueError(f"Invalid mood: {new_mood}")
        
        if not new_mood:
            # Random mood change
            character = self.db.query(Character).filter(Character.id == character_id).first()
            new_mood = self._determine_character_mood(character, user_id)
        
        mood = self.MOODS[new_mood].copy()
        mood["key"] = new_mood
        mood["triggered"] = True
        mood["started_at"] = datetime.utcnow()
        
        return {
            "success": True,
            "new_mood": mood,
            "message": f"Character mood changed to {mood['name']} {mood['emoji']}"
        }
    
    def get_all_moods(self) -> Dict:
        """Get information about all available moods"""
        return {
            "moods": [
                {
                    "key": key,
                    "name": mood["name"],
                    "emoji": mood["emoji"],
                    "description": mood["description"],
                    "effects": mood["effects"]
                }
                for key, mood in self.MOODS.items()
            ]
        }
    
    def get_mood_recommendations(self, character_id: int) -> List[str]:
        """Get mood recommendations based on character personality"""
        character = self.db.query(Character).filter(Character.id == character_id).first()
        if not character:
            return ["happy", "flirty"]
        
        recommendations = []
        
        # Recommend based on character traits
        if hasattr(character, 'traits') and character.traits:
            traits = character.traits if isinstance(character.traits, dict) else {}
            
            if traits.get("flirty", 0) > 7:
                recommendations.append("flirty")
            if traits.get("romantic", 0) > 7:
                recommendations.append("romantic")
            if traits.get("energetic", 0) > 7:
                recommendations.append("energetic")
            if traits.get("mysterious", 0) > 7:
                recommendations.append("mysterious")
        
        # Recommend based on conversation style
        if hasattr(character, 'conversation_style'):
            style_mood_map = {
                "flirty": "flirty",
                "romantic": "romantic",
                "energetic": "energetic",
                "mystical": "mysterious",
                "zen": "contemplative"
            }
            
            if character.conversation_style in style_mood_map:
                mood = style_mood_map[character.conversation_style]
                if mood not in recommendations:
                    recommendations.append(mood)
        
        # Default recommendations
        if not recommendations:
            recommendations = ["happy", "flirty", "romantic"]
        
        return recommendations[:3]  # Return top 3 recommendations
