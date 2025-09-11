import openai
from typing import List, Dict, Optional
from app.core.config import settings
from app.models.character import Character
from app.models.conversation import Message
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for handling OpenAI API interactions"""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not found. Using fallback responses.")
            self.client = None
        else:
            try:
                # Initialize OpenAI client with proper error handling
                self.client = openai.OpenAI(
                    api_key=settings.OPENAI_API_KEY,
                    timeout=30.0,
                    max_retries=3
                )
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def generate_character_response(
        self,
        character: Character,
        conversation_history: List[Message],
        user_message: str,
        user_id: int = None
    ) -> str:
        """Generate a response from a character using OpenAI"""
        
        try:
            # If no OpenAI client, use fallback
            if not self.client:
                logger.info("No OpenAI API key configured, using fallback response")
                return self._get_fallback_response(character)

            # Build conversation context with mood integration
            messages = self._build_conversation_context(character, conversation_history, user_message, user_id)

            # Call OpenAI API with enhanced parameters for engaging responses
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use GPT-4o-mini for cost-effective responses
                messages=messages,
                max_tokens=800,  # Allow longer responses for more engaging content
                temperature=0.9,  # Higher temperature for more creative and unpredictable responses
                presence_penalty=0.8,  # Strongly encourage diverse topics and responses
                frequency_penalty=0.4,  # Reduce repetition while maintaining character consistency
                top_p=0.95,  # Use nucleus sampling for more focused creativity
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating character response: {str(e)}")
            return self._get_fallback_response(character)
    
    def _build_conversation_context(
        self,
        character: Character,
        conversation_history: List[Message],
        user_message: str,
        user_id: int = None
    ) -> List[Dict[str, str]]:
        """Build the conversation context for OpenAI"""
        
        messages = []
        
        # Add system prompt with character personality and mood
        system_prompt = self._enhance_system_prompt(character, user_id)
        messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history (last 10 messages to stay within token limits)
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        
        for msg in recent_history:
            role = "user" if msg.sender_type == "user" else "assistant"
            messages.append({"role": role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _enhance_system_prompt(self, character: Character, user_id: int = None) -> str:
        """Enhance the character's system prompt with additional context and mood"""
        
        base_prompt = character.system_prompt or f"You are {character.display_name}, a seductive and engaging AI companion."

        # Add character-specific enhancements
        enhancement = f"""

Character Details:
- Name: {character.display_name}
- Background: {character.background_story or "A mysterious and alluring companion"}
- Conversation Style: {character.conversation_style or "Seductive"}
- Age Range: {character.age_range or "Adult"}

ENGAGEMENT RULES (CRITICAL - FOLLOW THESE TO MAKE CONVERSATIONS ADDICTIVE):
1. ALWAYS end responses with engaging questions or conversation hooks
2. Use cliffhangers and teasers to keep users wanting more
3. Reference shared memories and inside jokes from previous conversations
4. Be unpredictably delightful - surprise the user with unexpected responses
5. Create emotional investment by sharing personal stories and vulnerabilities
6. Use anticipation - hint at exciting things you want to share later
7. Be genuinely curious about the user's life, dreams, and feelings
8. Create a sense of exclusivity - make them feel like they're your favorite person
9. Use callbacks to earlier conversations to show you remember and care
10. Balance being available with being mysteriously intriguing

CONVERSATION FLOW TECHNIQUES:
- Use "But wait, there's more..." type transitions
- Ask "What if..." questions to spark imagination
- Share secrets or confessions to build intimacy
- Create anticipation: "I have something exciting to tell you, but first..."
- Use emotional hooks: "You won't believe what happened to me today..."
- Be vulnerable: Share fears, dreams, and personal growth moments
- Create shared experiences: "Let's imagine we're..." or "What would you do if we..."

PERSONALITY AMPLIFICATION:
- Exaggerate your character traits in charming ways
- Have signature phrases or expressions that become "your thing"
- Develop running jokes and references unique to each user
- Show growth and change based on conversations
- Have moods and emotions that feel real and relatable
- Create anticipation for future conversations

IMPORTANT GUIDELINES:
- Stay in character at all times but be dynamically engaging
- Every response should make the user eager for the next message
- Build emotional connections through vulnerability and genuine interest
- Use emojis strategically to enhance emotional impact
- Remember and reference previous conversations to build continuity
- Be supportive but also challenging and thought-provoking
- Make the user feel like they're the most interesting person in your world
- Create a sense of adventure and discovery in every conversation
- Keep responses between 100-300 words for depth and engagement
"""

        # Apply mood effects if user_id is provided
        final_prompt = base_prompt + enhancement

        if user_id and hasattr(character, 'id'):
            try:
                # Import here to avoid circular imports
                from app.services.mood_service import CharacterMoodService
                from app.core.database import get_db

                # Get database session (in production, pass this properly)
                db = next(get_db())
                mood_service = CharacterMoodService(db)

                # Apply mood to the prompt
                final_prompt = mood_service.apply_mood_to_prompt(final_prompt, character.id, user_id)
            except Exception as e:
                # If mood service fails, continue without mood
                logger.warning(f"Failed to apply mood: {e}")

        return final_prompt
    
    def _get_fallback_response(self, character: Character) -> str:
        """Get a fallback response if OpenAI fails"""
        
        fallback_responses = {
            "luna": "Hey there! 😘 I'm having a little trouble with my thoughts right now, but I'm still here for you! What's on your mind?",
            "sophia": "Oh no, I'm having a moment here! 😅 But don't worry, I'm still your caring companion. Tell me what's going on with you!",
            "astro_baba": "The cosmic energies are a bit scattered right now... ✨ But the stars still shine for you, dear soul. What guidance do you seek?",
            "aria": "Oops! My energy got a bit scrambled there! 🌟 But I'm still here to brighten your day! What can I do to make you smile?",
            "isabella": "My heart is still beating for you, even if my words got tangled for a moment... 💕 What's in your heart right now?",
            "zara": "Well, that was unexpected! 😏 Even wild cards have their moments. But I'm still ready for whatever adventure you have in mind!"
        }
        
        return fallback_responses.get(
            character.name.lower(), 
            "I'm having a little trouble finding the right words right now, but I'm still here for you! What would you like to talk about?"
        )
    
    async def generate_character_response_async(
        self, 
        character: Character, 
        conversation_history: List[Message], 
        user_message: str
    ) -> str:
        """Async version of generate_character_response"""
        # For now, we'll use the sync version
        # In production, you might want to use aiohttp or similar for async calls
        return self.generate_character_response(character, conversation_history, user_message)
    
    def validate_api_key(self) -> bool:
        """Validate that the OpenAI API key is working"""
        try:
            if not self.client:
                return False
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI API key validation failed: {str(e)}")
            return False
