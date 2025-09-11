import os
import hashlib
import requests
from typing import Dict, Optional
from pathlib import Path
import tempfile
from app.core.config import settings
from app.models.character import Character
import logging

logger = logging.getLogger(__name__)

class VoiceService:
    """Service for generating AI voice messages using text-to-speech"""
    
    # Character voice mappings (ElevenLabs voice IDs)
    CHARACTER_VOICES = {
        # Romantic Companions
        "luna": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella - young, friendly
            "voice_name": "Bella",
            "description": "Playful and charming voice"
        },
        "valentina": {
            "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni - sophisticated
            "voice_name": "Rachel", 
            "description": "Passionate and sophisticated voice"
        },
        "scarlett": {
            "voice_id": "MF3mGyEYCl7XYWbV9V6O",  # Elli - seductive
            "voice_name": "Elli",
            "description": "Sultry and seductive voice"
        },
        "elena": {
            "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi - gentle
            "voice_name": "Domi",
            "description": "Sweet and gentle voice"
        },
        "aurora": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella - dreamy
            "voice_name": "Bella",
            "description": "Dreamy and whimsical voice"
        },
        "victoria": {
            "voice_id": "ErXwobaYiN019PkySvjV",  # Rachel - elegant
            "voice_name": "Rachel",
            "description": "Elegant and refined voice"
        },
        
        # Flirty Chat
        "sophia": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella - sweet
            "voice_name": "Bella",
            "description": "Sweet and bubbly voice"
        },
        "maya": {
            "voice_id": "ErXwobaYiN019PkySvjV",  # Rachel - witty
            "voice_name": "Rachel",
            "description": "Quick-witted and clever voice"
        },
        "chloe": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella - playful
            "voice_name": "Bella",
            "description": "Mischievous and playful voice"
        },
        "jasmine": {
            "voice_id": "MF3mGyEYCl7XYWbV9V6O",  # Elli - sultry
            "voice_name": "Elli",
            "description": "Sultry and mysterious voice"
        },
        "riley": {
            "voice_id": "ErXwobaYiN019PkySvjV",  # Rachel - bold
            "voice_name": "Rachel",
            "description": "Bold and confident voice"
        },
        "amber": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella - cute
            "voice_name": "Bella",
            "description": "Adorably cute voice"
        },
        
        # Default voice for other characters
        "default": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella
            "voice_name": "Bella",
            "description": "Default friendly voice"
        }
    }
    
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voice_cache_dir = Path("voice_cache")
        self.voice_cache_dir.mkdir(exist_ok=True)
    
    def generate_voice_message(
        self, 
        text: str, 
        character: Character,
        user_id: int = None
    ) -> Dict:
        """Generate voice message for character response"""
        
        if not self.api_key:
            return {
                "success": False,
                "error": "Voice service not configured",
                "fallback_text": text
            }
        
        try:
            # Get character voice configuration
            character_name = character.name.lower() if character.name else "default"
            voice_config = self.CHARACTER_VOICES.get(character_name, self.CHARACTER_VOICES["default"])
            
            # Clean text for TTS (remove markdown, emojis, etc.)
            clean_text = self._clean_text_for_tts(text)
            
            # Check cache first
            cache_key = self._generate_cache_key(clean_text, voice_config["voice_id"])
            cached_file = self.voice_cache_dir / f"{cache_key}.mp3"
            
            if cached_file.exists():
                return {
                    "success": True,
                    "audio_url": f"/api/v1/voice/audio/{cache_key}.mp3",
                    "text": text,
                    "voice_name": voice_config["voice_name"],
                    "cached": True
                }
            
            # Generate new voice message
            audio_data = self._call_elevenlabs_api(clean_text, voice_config["voice_id"])
            
            if audio_data:
                # Save to cache
                with open(cached_file, "wb") as f:
                    f.write(audio_data)
                
                return {
                    "success": True,
                    "audio_url": f"/api/v1/voice/audio/{cache_key}.mp3",
                    "text": text,
                    "voice_name": voice_config["voice_name"],
                    "cached": False
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate voice",
                    "fallback_text": text
                }
                
        except Exception as e:
            logger.error(f"Voice generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_text": text
            }
    
    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text for text-to-speech conversion"""
        import re
        
        # Remove markdown formatting
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove *bold*
        text = re.sub(r'_([^_]+)_', r'\1', text)    # Remove _italic_
        text = re.sub(r'`([^`]+)`', r'\1', text)    # Remove `code`
        
        # Remove action text in brackets/parentheses
        text = re.sub(r'\*[^*]+\*', '', text)       # Remove *actions*
        text = re.sub(r'\([^)]*\)', '', text)       # Remove (actions)
        
        # Remove excessive emojis (keep some for natural speech)
        text = re.sub(r'[😀-🙏]{3,}', '😊', text)   # Replace emoji spam with single emoji
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Limit length for TTS (ElevenLabs has character limits)
        if len(text) > 500:
            text = text[:497] + "..."
        
        return text
    
    def _generate_cache_key(self, text: str, voice_id: str) -> str:
        """Generate cache key for voice file"""
        content = f"{text}_{voice_id}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _call_elevenlabs_api(self, text: str, voice_id: str) -> Optional[bytes]:
        """Call ElevenLabs API to generate speech"""
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"ElevenLabs API request failed: {e}")
            return None
    
    def get_character_voice_info(self, character_name: str) -> Dict:
        """Get voice information for a character"""
        character_name = character_name.lower()
        voice_config = self.CHARACTER_VOICES.get(character_name, self.CHARACTER_VOICES["default"])
        
        return {
            "character": character_name,
            "voice_name": voice_config["voice_name"],
            "description": voice_config["description"],
            "voice_id": voice_config["voice_id"]
        }
    
    def get_all_character_voices(self) -> Dict:
        """Get voice information for all characters"""
        return {
            "voices": [
                {
                    "character": char_name,
                    "voice_name": config["voice_name"],
                    "description": config["description"]
                }
                for char_name, config in self.CHARACTER_VOICES.items()
                if char_name != "default"
            ]
        }
    
    def get_voice_file(self, filename: str) -> Optional[bytes]:
        """Get cached voice file"""
        file_path = self.voice_cache_dir / filename
        
        if file_path.exists() and file_path.suffix == '.mp3':
            try:
                with open(file_path, "rb") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading voice file {filename}: {e}")
        
        return None
    
    def clear_voice_cache(self) -> Dict:
        """Clear voice message cache"""
        try:
            import shutil
            if self.voice_cache_dir.exists():
                shutil.rmtree(self.voice_cache_dir)
                self.voice_cache_dir.mkdir(exist_ok=True)
            
            return {
                "success": True,
                "message": "Voice cache cleared successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to clear cache: {e}"
            }
    
    def get_cache_stats(self) -> Dict:
        """Get voice cache statistics"""
        try:
            cache_files = list(self.voice_cache_dir.glob("*.mp3"))
            total_size = sum(f.stat().st_size for f in cache_files)
            
            return {
                "total_files": len(cache_files),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "cache_directory": str(self.voice_cache_dir)
            }
        except Exception as e:
            return {
                "error": f"Failed to get cache stats: {e}"
            }
    
    def test_voice_generation(self, text: str = "Hello! This is a test message.") -> Dict:
        """Test voice generation with default voice"""
        try:
            # Use default voice for testing
            voice_config = self.CHARACTER_VOICES["default"]
            clean_text = self._clean_text_for_tts(text)
            
            audio_data = self._call_elevenlabs_api(clean_text, voice_config["voice_id"])
            
            if audio_data:
                # Save test file
                test_file = self.voice_cache_dir / "test_voice.mp3"
                with open(test_file, "wb") as f:
                    f.write(audio_data)
                
                return {
                    "success": True,
                    "message": "Voice generation test successful",
                    "test_file": str(test_file),
                    "text_used": clean_text
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate test voice"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Voice test failed: {e}"
            }
