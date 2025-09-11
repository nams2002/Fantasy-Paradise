import os
import hashlib
import requests
from typing import Dict, Optional, List
from pathlib import Path
import tempfile
from app.core.config import settings
from app.models.character import Character
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

class ImageGenerationService:
    """Service for generating AI images using DALL-E and other models"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY  # DALL-E uses OpenAI API
        self.base_url = "https://api.openai.com/v1"
        self.image_cache_dir = Path("image_cache")
        self.image_cache_dir.mkdir(exist_ok=True)
    
    def generate_character_image(
        self, 
        prompt: str, 
        character: Character,
        user_id: int,
        style: str = "realistic"
    ) -> Dict:
        """Generate image based on user prompt and character context"""
        
        if not self.api_key:
            return {
                "success": False,
                "error": "Image generation service not configured",
                "fallback_message": "Image generation is not available at the moment."
            }
        
        try:
            # Enhance prompt with character context
            enhanced_prompt = self._enhance_prompt_with_character(prompt, character, style)
            
            # Check cache first
            cache_key = self._generate_cache_key(enhanced_prompt)
            cached_file = self.image_cache_dir / f"{cache_key}.png"
            
            if cached_file.exists():
                return {
                    "success": True,
                    "image_url": f"/api/v1/images/view/{cache_key}.png",
                    "prompt": prompt,
                    "enhanced_prompt": enhanced_prompt,
                    "character": character.display_name,
                    "style": style,
                    "cached": True
                }
            
            # Generate new image
            image_url = self._call_dalle_api(enhanced_prompt)
            
            if image_url:
                # Download and cache the image
                image_data = self._download_image(image_url)
                if image_data:
                    with open(cached_file, "wb") as f:
                        f.write(image_data)
                    
                    return {
                        "success": True,
                        "image_url": f"/api/v1/images/view/{cache_key}.png",
                        "prompt": prompt,
                        "enhanced_prompt": enhanced_prompt,
                        "character": character.display_name,
                        "style": style,
                        "cached": False
                    }
            
            return {
                "success": False,
                "error": "Failed to generate image",
                "fallback_message": "Unable to create image at this time. Please try again later."
            }
                
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_message": "Image generation failed. Please try a different prompt."
            }
    
    def _enhance_prompt_with_character(self, user_prompt: str, character: Character, style: str) -> str:
        """Enhance user prompt with character context and style"""
        
        # Character context mapping
        character_contexts = {
            "luna": "beautiful young woman with playful expression, charming smile",
            "valentina": "elegant sophisticated woman with passionate eyes, romantic atmosphere",
            "scarlett": "sultry seductive woman with confident pose, alluring gaze",
            "elena": "sweet gentle woman with kind eyes, warm smile",
            "aurora": "dreamy whimsical woman with ethereal beauty, magical atmosphere",
            "victoria": "refined elegant woman with classic beauty, sophisticated setting",
            "sophia": "cute bubbly woman with bright smile, youthful energy",
            "maya": "intelligent witty woman with clever expression, confident pose",
            "chloe": "playful mischievous woman with teasing smile, fun atmosphere",
            "jasmine": "mysterious sultry woman with enigmatic expression, exotic beauty",
            "riley": "bold confident woman with strong presence, empowering pose",
            "amber": "adorable cute woman with innocent charm, sweet expression",
            "aria": "energetic positive woman with bright smile, sunny atmosphere",
            "sunny": "optimistic cheerful woman with radiant smile, uplifting mood",
            "joy": "happy mindful woman with peaceful expression, serene setting",
            "bliss": "calm zen woman with tranquil pose, meditative atmosphere",
            "spark": "dynamic energetic woman with vibrant expression, exciting mood",
            "hope": "gentle encouraging woman with warm eyes, inspiring presence",
            "isabella": "mysterious vampire queen with dark beauty, gothic atmosphere",
            "seraphina": "angelic divine woman with ethereal glow, heavenly setting",
            "morgana": "powerful sorceress with magical aura, mystical atmosphere",
            "luna_wolf": "wild fierce woman with primal beauty, nature setting",
            "celeste": "otherworldly space princess with cosmic beauty, futuristic setting",
            "nyx": "dark mysterious woman with shadow magic, noir atmosphere"
        }
        
        # Style modifiers
        style_modifiers = {
            "realistic": "photorealistic, high quality, detailed",
            "anime": "anime style, manga art, vibrant colors",
            "artistic": "artistic painting, beautiful art style, creative",
            "fantasy": "fantasy art, magical, ethereal, mystical",
            "portrait": "professional portrait, studio lighting, elegant",
            "casual": "casual setting, natural lighting, relaxed pose"
        }
        
        # Get character context
        character_name = character.name.lower() if character.name else "default"
        character_context = character_contexts.get(character_name, "beautiful woman")
        
        # Get style modifier
        style_modifier = style_modifiers.get(style, "high quality, detailed")
        
        # Combine everything
        enhanced_prompt = f"{user_prompt}, featuring {character_context}, {style_modifier}, professional quality, safe for work"
        
        # Add safety filters
        enhanced_prompt += ", appropriate content, tasteful, elegant"
        
        return enhanced_prompt
    
    def _generate_cache_key(self, prompt: str) -> str:
        """Generate cache key for image"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def _call_dalle_api(self, prompt: str) -> Optional[str]:
        """Call DALL-E API to generate image"""
        
        url = f"{self.base_url}/images/generations"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "standard",
            "style": "natural"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("data") and len(result["data"]) > 0:
                    return result["data"][0]["url"]
            else:
                logger.error(f"DALL-E API error: {response.status_code} - {response.text}")
                
        except requests.RequestException as e:
            logger.error(f"DALL-E API request failed: {e}")
        
        return None
    
    def _download_image(self, url: str) -> Optional[bytes]:
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to download image: {e}")
        
        return None
    
    def get_image_file(self, filename: str) -> Optional[bytes]:
        """Get cached image file"""
        file_path = self.image_cache_dir / filename
        
        if file_path.exists() and file_path.suffix in ['.png', '.jpg', '.jpeg']:
            try:
                with open(file_path, "rb") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading image file {filename}: {e}")
        
        return None
    
    def get_character_image_suggestions(self, character: Character) -> List[str]:
        """Get image prompt suggestions for character"""
        
        character_suggestions = {
            "luna": [
                "Luna sitting in a cozy cafe with a playful smile",
                "Luna in a beautiful garden with flowers",
                "Luna wearing a cute summer dress",
                "Luna at sunset with a charming expression"
            ],
            "valentina": [
                "Valentina in an elegant evening gown",
                "Valentina by candlelight with roses",
                "Valentina in a romantic restaurant setting",
                "Valentina in a luxurious ballroom"
            ],
            "scarlett": [
                "Scarlett in a sophisticated black dress",
                "Scarlett with dramatic lighting and shadows",
                "Scarlett in an upscale lounge setting",
                "Scarlett with a confident, alluring pose"
            ],
            "isabella": [
                "Isabella in a gothic castle setting",
                "Isabella with dark romantic atmosphere",
                "Isabella in Victorian-era clothing",
                "Isabella under moonlight with mysterious aura"
            ],
            "aria": [
                "Aria in a bright, sunny meadow",
                "Aria with colorful balloons and confetti",
                "Aria in workout clothes with energetic pose",
                "Aria at a fun carnival or festival"
            ]
        }
        
        character_name = character.name.lower() if character.name else "default"
        suggestions = character_suggestions.get(character_name, [
            "Beautiful portrait in natural lighting",
            "Casual outfit in a cozy setting",
            "Elegant dress in a fancy location",
            "Fun activity or hobby scene"
        ])
        
        return suggestions
    
    def get_style_options(self) -> Dict:
        """Get available image styles"""
        return {
            "styles": [
                {
                    "id": "realistic",
                    "name": "Realistic",
                    "description": "Photorealistic, high-quality images",
                    "example": "Professional photo quality"
                },
                {
                    "id": "anime",
                    "name": "Anime",
                    "description": "Anime/manga art style",
                    "example": "Japanese animation style"
                },
                {
                    "id": "artistic",
                    "name": "Artistic",
                    "description": "Artistic painting style",
                    "example": "Beautiful art painting"
                },
                {
                    "id": "fantasy",
                    "name": "Fantasy",
                    "description": "Magical, mystical atmosphere",
                    "example": "Fantasy art with magical elements"
                },
                {
                    "id": "portrait",
                    "name": "Portrait",
                    "description": "Professional portrait style",
                    "example": "Studio portrait with elegant lighting"
                },
                {
                    "id": "casual",
                    "name": "Casual",
                    "description": "Natural, relaxed setting",
                    "example": "Everyday casual scene"
                }
            ]
        }
    
    def clear_image_cache(self) -> Dict:
        """Clear image cache"""
        try:
            import shutil
            if self.image_cache_dir.exists():
                shutil.rmtree(self.image_cache_dir)
                self.image_cache_dir.mkdir(exist_ok=True)
            
            return {
                "success": True,
                "message": "Image cache cleared successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to clear cache: {e}"
            }
    
    def get_cache_stats(self) -> Dict:
        """Get image cache statistics"""
        try:
            cache_files = list(self.image_cache_dir.glob("*.png"))
            total_size = sum(f.stat().st_size for f in cache_files)
            
            return {
                "total_files": len(cache_files),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "cache_directory": str(self.image_cache_dir)
            }
        except Exception as e:
            return {
                "error": f"Failed to get cache stats: {e}"
            }
    
    def test_image_generation(self, prompt: str = "A beautiful sunset over mountains") -> Dict:
        """Test image generation"""
        try:
            enhanced_prompt = f"{prompt}, high quality, detailed, safe for work"
            image_url = self._call_dalle_api(enhanced_prompt)
            
            if image_url:
                return {
                    "success": True,
                    "message": "Image generation test successful",
                    "test_image_url": image_url,
                    "prompt_used": enhanced_prompt
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate test image"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Image test failed: {e}"
            }
