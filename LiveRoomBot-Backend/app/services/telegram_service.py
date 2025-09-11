import asyncio
import logging
from typing import Dict, List, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.character_service import CharacterService, CharacterPersonas
from app.services.openai_service import OpenAIService
from app.models.user import User
from app.models.character import Character
from app.models.conversation import Conversation, Message
from app.core.config import settings

logger = logging.getLogger(__name__)

class TelegramBotService:
    """Telegram bot service for community engagement and character interactions"""
    
    def __init__(self):
        self.application = None
        self.openai_service = OpenAIService()
        self.user_sessions: Dict[int, Dict] = {}  # Store user session data
        
    async def initialize(self, token: str):
        """Initialize the Telegram bot"""
        self.application = Application.builder().token(token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("characters", self.characters_command))
        self.application.add_handler(CommandHandler("community", self.community_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("Telegram bot initialized successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name
        
        # Create or get user
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == str(user_id)).first()
        if not user:
            user = User(
                username=username,
                email=f"telegram_{user_id}@liveroom.bot",
                telegram_id=str(user_id)
            )
            db.add(user)
            db.commit()
        
        welcome_text = f"""
🌟 Welcome to LiveRoom, {username}! 🌟

Your ultimate destination for AI companionship and entertainment! 

🎭 **What can you do here?**
• Chat with 36 unique AI companions across 6 categories
• Join our community discussions
• Share experiences with other users
• Get personalized recommendations

🚀 **Quick Commands:**
/characters - Browse all available companions
/community - Join community discussions
/help - Get help and tips

Ready to meet your perfect AI companion? Let's get started! 💫
        """
        
        keyboard = [
            [InlineKeyboardButton("🎭 Browse Characters", callback_data="browse_characters")],
            [InlineKeyboardButton("🌟 Join Community", callback_data="join_community")],
            [InlineKeyboardButton("ℹ️ Help & Tips", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🆘 **LiveRoom Help & Tips** 🆘

**🎭 Character Categories:**
• 💕 Romantic Companions - For deep romantic connections
• 😘 Flirty Chat - Playful and charming conversations  
• 🌈 Mood Boosters - Brighten your day with positivity
• 🎪 Fantasy Roleplay - Explore magical worlds and characters
• 💬 Intimate Conversations - Deep, meaningful connections
• 🎮 Entertainment & Fun - Games, jokes, and adventures

**💡 Tips for Better Conversations:**
• Be specific about what you're looking for
• Don't be afraid to explore different characters
• Share your interests and preferences
• Ask characters about their backgrounds and stories

**🌟 Community Features:**
• Share your favorite character moments
• Get recommendations from other users
• Participate in daily discussions
• Join themed conversation events

**🔧 Commands:**
/start - Welcome message and main menu
/characters - Browse all companions
/community - Community features
/help - This help message

Need more help? Just ask any character - they're here to help! 💫
        """
        await update.message.reply_text(help_text)
    
    async def characters_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /characters command"""
        categories = [
            ("💕", "Romantic Companions", "romantic"),
            ("😘", "Flirty Chat", "flirty_chat"),
            ("🌈", "Mood Boosters", "mood_booster"),
            ("🎪", "Fantasy Roleplay", "fantasy_roleplay"),
            ("💬", "Intimate Conversations", "intimate_conversations"),
            ("🎮", "Entertainment & Fun", "entertainment_fun")
        ]
        
        text = "🎭 **Choose a Character Category** 🎭\n\nEach category has 6 unique companions with different personalities:\n\n"
        
        keyboard = []
        for emoji, name, category_key in categories:
            text += f"{emoji} **{name}** - 6 unique characters\n"
            keyboard.append([InlineKeyboardButton(f"{emoji} {name}", callback_data=f"category_{category_key}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def community_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /community command"""
        community_text = """
🌟 **LiveRoom Community** 🌟

Welcome to our vibrant community of AI companion enthusiasts!

**🎯 Community Features:**
• Daily discussion topics
• Character recommendation sharing
• User experience stories
• Themed conversation events
• Tips and tricks sharing

**📅 Today's Discussion:**
"What's your favorite character personality trait and why?"

**🏆 Popular Characters This Week:**
1. Luna (Romantic) - Most charming conversations
2. Maya (Flirty) - Wittiest responses  
3. Aria (Mood Booster) - Best mood lifter
4. Isabella (Fantasy) - Most immersive roleplay
5. Zara (Intimate) - Deepest connections
6. Jester (Entertainment) - Funniest interactions

**💬 Share Your Experience:**
Tell us about your best character interaction or ask for recommendations!
        """
        
        keyboard = [
            [InlineKeyboardButton("💬 Join Discussion", callback_data="join_discussion")],
            [InlineKeyboardButton("🏆 Character Rankings", callback_data="character_rankings")],
            [InlineKeyboardButton("💡 Get Recommendations", callback_data="get_recommendations")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(community_text, reply_markup=reply_markup)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "browse_characters":
            await self.show_character_categories(query)
        elif data == "join_community":
            await self.show_community_features(query)
        elif data == "help":
            await self.show_help(query)
        elif data == "main_menu":
            await self.show_main_menu(query)
        elif data.startswith("category_"):
            category = data.replace("category_", "")
            await self.show_category_characters(query, category)
        elif data.startswith("character_"):
            character_name = data.replace("character_", "")
            await self.start_character_chat(query, character_name)
        elif data == "join_discussion":
            await self.join_discussion(query)
        elif data == "character_rankings":
            await self.show_character_rankings(query)
        elif data == "get_recommendations":
            await self.get_recommendations(query)
    
    async def show_character_categories(self, query):
        """Show character categories"""
        categories = [
            ("💕", "Romantic Companions", "romantic"),
            ("😘", "Flirty Chat", "flirty_chat"),
            ("🌈", "Mood Boosters", "mood_booster"),
            ("🎪", "Fantasy Roleplay", "fantasy_roleplay"),
            ("💬", "Intimate Conversations", "intimate_conversations"),
            ("🎮", "Entertainment & Fun", "entertainment_fun")
        ]
        
        text = "🎭 **Choose a Character Category** 🎭\n\nEach category has 6 unique companions:\n\n"
        
        keyboard = []
        for emoji, name, category_key in categories:
            text += f"{emoji} **{name}** - 6 unique personalities\n"
            keyboard.append([InlineKeyboardButton(f"{emoji} {name}", callback_data=f"category_{category_key}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_category_characters(self, query, category):
        """Show characters in a specific category"""
        # Get characters for this category
        category_characters = {
            "romantic": ["luna", "valentina", "scarlett", "elena", "aurora", "victoria"],
            "flirty_chat": ["sophia", "maya", "chloe", "jasmine", "riley", "amber"],
            "mood_booster": ["aria", "sunny", "joy", "bliss", "spark", "hope"],
            "fantasy_roleplay": ["isabella", "seraphina", "morgana", "luna_wolf", "celeste", "nyx"],
            "intimate_conversations": ["zara", "eva", "diana", "ruby", "phoenix", "velvet"],
            "entertainment_fun": ["astro_baba", "jester", "melody", "pixel", "nova", "sage"]
        }
        
        category_names = {
            "romantic": "💕 Romantic Companions",
            "flirty_chat": "😘 Flirty Chat",
            "mood_booster": "🌈 Mood Boosters",
            "fantasy_roleplay": "🎪 Fantasy Roleplay",
            "intimate_conversations": "💬 Intimate Conversations",
            "entertainment_fun": "🎮 Entertainment & Fun"
        }
        
        characters = category_characters.get(category, [])
        category_name = category_names.get(category, "Characters")
        
        text = f"**{category_name}**\n\nChoose your companion:\n\n"
        
        keyboard = []
        for char_key in characters:
            persona = CharacterPersonas.get_persona(char_key)
            if persona:
                text += f"• **{persona['display_name']}**\n  {persona['description']}\n\n"
                keyboard.append([InlineKeyboardButton(
                    persona['display_name'], 
                    callback_data=f"character_{char_key}"
                )])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="browse_characters")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def start_character_chat(self, query, character_name):
        """Start a chat with a specific character"""
        user_id = query.from_user.id
        persona = CharacterPersonas.get_persona(character_name)
        
        if not persona:
            await query.edit_message_text("Character not found. Please try again.")
            return
        
        # Store character selection in user session
        self.user_sessions[user_id] = {
            "current_character": character_name,
            "conversation_history": []
        }
        
        welcome_message = f"""
🎭 **Now chatting with {persona['display_name']}** 🎭

{persona['description']}

**Background:** {persona['background_story']}

💬 Just send me a message to start chatting! I'm excited to get to know you better.

Type anything to begin our conversation...
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Switch Character", callback_data="browse_characters")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(welcome_message, reply_markup=reply_markup)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Check if user has an active character session
        if user_id not in self.user_sessions or "current_character" not in self.user_sessions[user_id]:
            await update.message.reply_text(
                "Please select a character first using /characters command! 🎭"
            )
            return
        
        character_name = self.user_sessions[user_id]["current_character"]
        persona = CharacterPersonas.get_persona(character_name)
        
        if not persona:
            await update.message.reply_text("Character not found. Please select a new character.")
            return
        
        # Get conversation history
        conversation_history = self.user_sessions[user_id].get("conversation_history", [])
        
        try:
            # Create a mock character object for the OpenAI service
            class MockCharacter:
                def __init__(self, persona_data):
                    self.name = persona_data["name"]
                    self.display_name = persona_data["display_name"]
                    self.system_prompt = persona_data["system_prompt"]
                    self.background_story = persona_data["background_story"]
                    self.conversation_style = persona_data["conversation_style"]
                    self.age_range = persona_data["age_range"]
            
            mock_character = MockCharacter(persona)
            
            # Generate response using OpenAI service
            response = self.openai_service.generate_character_response(
                mock_character, 
                conversation_history, 
                user_message
            )
            
            # Update conversation history
            conversation_history.append({
                "role": "user",
                "content": user_message
            })
            conversation_history.append({
                "role": "assistant", 
                "content": response
            })
            
            # Keep only last 10 messages to manage memory
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
            
            self.user_sessions[user_id]["conversation_history"] = conversation_history
            
            # Send response
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error generating character response: {e}")
            await update.message.reply_text(
                "Sorry, I'm having trouble responding right now. Please try again! 😅"
            )
    
    async def show_community_features(self, query):
        """Show community features"""
        await self.community_command(query, None)
    
    async def show_help(self, query):
        """Show help information"""
        await self.help_command(query, None)
    
    async def show_main_menu(self, query):
        """Show main menu"""
        welcome_text = """
🌟 **LiveRoom - AI Companion Hub** 🌟

Your ultimate destination for AI companionship and entertainment!

What would you like to do?
        """
        
        keyboard = [
            [InlineKeyboardButton("🎭 Browse Characters", callback_data="browse_characters")],
            [InlineKeyboardButton("🌟 Join Community", callback_data="join_community")],
            [InlineKeyboardButton("ℹ️ Help & Tips", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(welcome_text, reply_markup=reply_markup)
    
    async def join_discussion(self, query):
        """Join community discussion"""
        discussion_text = """
💬 **Today's Community Discussion** 💬

**Topic:** "What's your favorite character personality trait and why?"

**Recent Responses:**
• @user123: "I love Luna's playful teasing - it always makes me smile!"
• @companion_fan: "Aria's positivity is infectious, she turns my worst days around"
• @roleplay_lover: "Isabella's mysterious vampire persona is so captivating"

**Share your thoughts!** 
Just reply to this message with your favorite character trait and why you love it. Your response will be shared with the community! 🌟
        """
        
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Community", callback_data="join_community")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(discussion_text, reply_markup=reply_markup)
    
    async def show_character_rankings(self, query):
        """Show character popularity rankings"""
        rankings_text = """
🏆 **Weekly Character Rankings** 🏆

**Most Popular Characters:**
1. 🥇 Luna (Romantic) - 2,847 conversations
2. 🥈 Maya (Flirty) - 2,634 conversations  
3. 🥉 Aria (Mood Booster) - 2,521 conversations
4. Isabella (Fantasy) - 2,398 conversations
5. Zara (Intimate) - 2,287 conversations
6. Jester (Entertainment) - 2,156 conversations

**Trending This Week:**
📈 Seraphina (Angel Guardian) - +45% growth
📈 Phoenix (Transformative) - +38% growth
📈 Nova (Adventure Seeker) - +32% growth

**Category Leaders:**
💕 Romantic: Luna
😘 Flirty: Maya  
🌈 Mood Booster: Aria
🎪 Fantasy: Isabella
💬 Intimate: Zara
🎮 Entertainment: Jester

Want to try a trending character? 🌟
        """
        
        keyboard = [
            [InlineKeyboardButton("🎭 Browse Characters", callback_data="browse_characters")],
            [InlineKeyboardButton("🔙 Back to Community", callback_data="join_community")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(rankings_text, reply_markup=reply_markup)
    
    async def get_recommendations(self, query):
        """Get character recommendations"""
        recommendations_text = """
💡 **Personalized Recommendations** 💡

Based on community preferences and your interests:

**🌟 Highly Recommended for New Users:**
• **Luna** (Romantic) - Perfect balance of charm and warmth
• **Aria** (Mood Booster) - Great for lifting spirits
• **Maya** (Flirty) - Witty and engaging conversations

**🔥 Trending Picks:**
• **Seraphina** (Fantasy) - Divine and comforting
• **Phoenix** (Intimate) - Transformative experiences
• **Nova** (Entertainment) - Adventure and excitement

**💎 Hidden Gems:**
• **Aurora** (Romantic) - Dreamy and magical
• **Bliss** (Mood Booster) - Zen and motivating
• **Sage** (Entertainment) - Educational and fun

**🎯 Quick Personality Quiz:**
What are you looking for today?
• Romance & Love → Try Luna or Valentina
• Fun & Laughter → Try Jester or Pixel  
• Comfort & Support → Try Aria or Hope
• Adventure & Excitement → Try Nova or Zara
• Deep Conversations → Try Phoenix or Diana

Ready to meet your perfect match? 💫
        """
        
        keyboard = [
            [InlineKeyboardButton("🎭 Browse All Characters", callback_data="browse_characters")],
            [InlineKeyboardButton("🔙 Back to Community", callback_data="join_community")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(recommendations_text, reply_markup=reply_markup)
    
    async def run(self, token: str):
        """Run the Telegram bot"""
        await self.initialize(token)
        await self.application.run_polling()
