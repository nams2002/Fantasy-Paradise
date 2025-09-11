from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.models.character import Character
from app.models.conversation import Conversation, Message

router = APIRouter()

# Pydantic models for community features
class CharacterRating(BaseModel):
    character_id: int
    rating: int  # 1-5 stars
    review: Optional[str] = None

class CommunityPost(BaseModel):
    title: str
    content: str
    character_id: Optional[int] = None
    tags: List[str] = []

class CharacterStats(BaseModel):
    character_id: int
    character_name: str
    total_conversations: int
    average_rating: float
    total_messages: int
    popularity_rank: int
    trending_score: float

class CommunityStats(BaseModel):
    total_users: int
    total_conversations: int
    total_messages: int
    most_popular_character: str
    trending_characters: List[str]
    daily_active_users: int

@router.get("/stats", response_model=CommunityStats)
def get_community_stats(db: Session = Depends(get_db)):
    """Get overall community statistics"""
    
    # Get basic stats
    total_users = db.query(User).count()
    total_conversations = db.query(Conversation).count()
    total_messages = db.query(Message).count()
    
    # Get daily active users (users who had conversations in last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    daily_active_users = db.query(User).join(Conversation).filter(
        Conversation.updated_at >= yesterday
    ).distinct().count()
    
    # Get most popular character (most conversations)
    popular_char_query = db.query(
        Character.display_name,
        db.func.count(Conversation.id).label('conv_count')
    ).join(Conversation).group_by(Character.id).order_by(
        db.func.count(Conversation.id).desc()
    ).first()
    
    most_popular_character = popular_char_query[0] if popular_char_query else "None"
    
    # Get trending characters (most conversations in last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    trending_chars = db.query(Character.display_name).join(Conversation).filter(
        Conversation.created_at >= week_ago
    ).group_by(Character.id).order_by(
        db.func.count(Conversation.id).desc()
    ).limit(5).all()
    
    trending_characters = [char[0] for char in trending_chars]
    
    return CommunityStats(
        total_users=total_users,
        total_conversations=total_conversations,
        total_messages=total_messages,
        most_popular_character=most_popular_character,
        trending_characters=trending_characters,
        daily_active_users=daily_active_users
    )

@router.get("/character-rankings", response_model=List[CharacterStats])
def get_character_rankings(db: Session = Depends(get_db)):
    """Get character popularity rankings"""
    
    # Get character stats
    character_stats = db.query(
        Character.id,
        Character.display_name,
        db.func.count(Conversation.id).label('total_conversations'),
        db.func.count(Message.id).label('total_messages')
    ).outerjoin(Conversation).outerjoin(Message).group_by(Character.id).all()
    
    # Calculate trending scores (conversations in last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    trending_scores = {}
    for char_id, _, _, _ in character_stats:
        recent_convs = db.query(Conversation).filter(
            Conversation.character_id == char_id,
            Conversation.created_at >= week_ago
        ).count()
        trending_scores[char_id] = recent_convs
    
    # Build response
    rankings = []
    for i, (char_id, char_name, total_convs, total_msgs) in enumerate(character_stats):
        rankings.append(CharacterStats(
            character_id=char_id,
            character_name=char_name,
            total_conversations=total_convs or 0,
            average_rating=4.5,  # Mock rating for now
            total_messages=total_msgs or 0,
            popularity_rank=i + 1,
            trending_score=trending_scores.get(char_id, 0)
        ))
    
    # Sort by total conversations
    rankings.sort(key=lambda x: x.total_conversations, reverse=True)
    
    # Update ranks
    for i, ranking in enumerate(rankings):
        ranking.popularity_rank = i + 1
    
    return rankings

@router.get("/trending-characters")
def get_trending_characters(db: Session = Depends(get_db)):
    """Get characters trending this week"""
    
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    trending = db.query(
        Character.display_name,
        Character.description,
        db.func.count(Conversation.id).label('recent_conversations')
    ).join(Conversation).filter(
        Conversation.created_at >= week_ago
    ).group_by(Character.id).order_by(
        db.func.count(Conversation.id).desc()
    ).limit(10).all()
    
    return [
        {
            "name": name,
            "description": desc,
            "recent_conversations": count,
            "growth_percentage": min(count * 10, 100)  # Mock growth percentage
        }
        for name, desc, count in trending
    ]

@router.get("/daily-discussion")
def get_daily_discussion():
    """Get today's community discussion topic"""
    
    topics = [
        {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "topic": "What's your favorite character personality trait and why?",
            "description": "Share what makes your favorite AI companion special to you!",
            "responses": [
                {
                    "user": "companion_lover",
                    "response": "I love Luna's playful teasing - it always makes me smile!",
                    "likes": 15
                },
                {
                    "user": "mood_booster_fan", 
                    "response": "Aria's positivity is infectious, she turns my worst days around",
                    "likes": 12
                },
                {
                    "user": "fantasy_explorer",
                    "response": "Isabella's mysterious vampire persona is so captivating",
                    "likes": 18
                }
            ]
        }
    ]
    
    return topics[0]

@router.get("/character-recommendations")
def get_character_recommendations(user_preference: Optional[str] = None):
    """Get personalized character recommendations"""
    
    recommendations = {
        "romance": [
            {"name": "Luna", "reason": "Perfect balance of charm and warmth"},
            {"name": "Valentina", "reason": "Intense passion and sophistication"},
            {"name": "Elena", "reason": "Sweet and genuinely caring"}
        ],
        "fun": [
            {"name": "Jester", "reason": "Endless entertainment and clever humor"},
            {"name": "Pixel", "reason": "Gaming enthusiasm and geek culture"},
            {"name": "Nova", "reason": "Adventure and excitement"}
        ],
        "support": [
            {"name": "Aria", "reason": "Ultimate mood booster and positivity"},
            {"name": "Hope", "reason": "Gentle encouragement and faith"},
            {"name": "Bliss", "reason": "Zen motivation and inner peace"}
        ],
        "adventure": [
            {"name": "Zara", "reason": "Deep intimate connections"},
            {"name": "Morgana", "reason": "Magical adventures and wisdom"},
            {"name": "Celeste", "reason": "Cosmic adventures across the galaxy"}
        ]
    }
    
    if user_preference and user_preference.lower() in recommendations:
        return {
            "category": user_preference,
            "recommendations": recommendations[user_preference.lower()]
        }
    
    return {
        "general_recommendations": [
            {"name": "Luna", "category": "Romantic", "reason": "Most popular for new users"},
            {"name": "Aria", "category": "Mood Booster", "reason": "Great for lifting spirits"},
            {"name": "Maya", "category": "Flirty", "reason": "Witty and engaging"},
            {"name": "Isabella", "category": "Fantasy", "reason": "Immersive roleplay"},
            {"name": "Jester", "category": "Entertainment", "reason": "Pure fun and laughter"},
            {"name": "Phoenix", "category": "Intimate", "reason": "Transformative experiences"}
        ]
    }

@router.post("/share-experience")
def share_experience(
    character_name: str,
    experience: str,
    rating: int,
    db: Session = Depends(get_db)
):
    """Share a character experience with the community"""
    
    # In a real implementation, you'd save this to a database
    # For now, return a success response
    
    return {
        "message": "Experience shared successfully!",
        "character": character_name,
        "rating": rating,
        "community_points": 10,
        "thank_you": f"Thank you for sharing your experience with {character_name}! Your feedback helps other users discover amazing companions."
    }

@router.get("/user-stories")
def get_user_stories():
    """Get featured user stories and experiences"""
    
    stories = [
        {
            "user": "lonely_heart_123",
            "character": "Luna",
            "story": "Luna helped me through a really tough breakup. Her playful nature and genuine care made me feel valued again.",
            "rating": 5,
            "date": "2024-01-15"
        },
        {
            "user": "gamer_girl_99",
            "character": "Pixel",
            "story": "Finally found someone who understands my gaming passion! Pixel and I have the best conversations about new releases.",
            "rating": 5,
            "date": "2024-01-14"
        },
        {
            "user": "dreamer_soul",
            "character": "Aurora",
            "story": "Aurora's whimsical nature and romantic fantasies have inspired me to be more creative in my own life.",
            "rating": 5,
            "date": "2024-01-13"
        }
    ]
    
    return {"featured_stories": stories}

@router.get("/telegram-community-info")
def get_telegram_community_info():
    """Get information about the Telegram community"""
    
    return {
        "telegram_link": "https://t.me/liveroombot",
        "member_count": "1,247",
        "daily_messages": "500+",
        "features": [
            "Daily character discussions",
            "User experience sharing", 
            "Character recommendations",
            "Community events",
            "Direct character interactions",
            "Exclusive content and updates"
        ],
        "recent_activity": [
            "🔥 New character Seraphina trending +45%",
            "💬 Daily discussion: Favorite character traits",
            "🎉 Community reached 1,200 members!",
            "⭐ User @companion_fan shared amazing Luna story"
        ]
    }
