from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
import json

class GamificationService:
    """Service for managing user gamification features like badges, achievements, and streaks"""
    
    # Badge definitions
    BADGES = {
        # Conversation Badges
        "first_chat": {
            "name": "First Chat",
            "description": "Started your first conversation",
            "emoji": "💬",
            "category": "conversation",
            "points": 10,
            "requirement": "Send 1 message"
        },
        "chatty": {
            "name": "Chatty",
            "description": "Sent 100 messages",
            "emoji": "🗣️",
            "category": "conversation", 
            "points": 50,
            "requirement": "Send 100 messages"
        },
        "conversation_master": {
            "name": "Conversation Master",
            "description": "Sent 1000 messages",
            "emoji": "🎭",
            "category": "conversation",
            "points": 200,
            "requirement": "Send 1000 messages"
        },
        
        # Character Badges
        "character_explorer": {
            "name": "Character Explorer",
            "description": "Chatted with 5 different characters",
            "emoji": "🌟",
            "category": "character",
            "points": 30,
            "requirement": "Chat with 5 characters"
        },
        "character_collector": {
            "name": "Character Collector",
            "description": "Chatted with all 36 characters",
            "emoji": "🏆",
            "category": "character",
            "points": 500,
            "requirement": "Chat with all characters"
        },
        "romantic_soul": {
            "name": "Romantic Soul",
            "description": "Spent quality time with romantic characters",
            "emoji": "💕",
            "category": "character",
            "points": 40,
            "requirement": "100 messages with romantic characters"
        },
        "flirt_master": {
            "name": "Flirt Master",
            "description": "Master of flirty conversations",
            "emoji": "😘",
            "category": "character",
            "points": 40,
            "requirement": "100 messages with flirty characters"
        },
        
        # Streak Badges
        "daily_visitor": {
            "name": "Daily Visitor",
            "description": "Logged in for 7 days straight",
            "emoji": "📅",
            "category": "streak",
            "points": 70,
            "requirement": "7-day login streak"
        },
        "dedicated_user": {
            "name": "Dedicated User",
            "description": "Logged in for 30 days straight",
            "emoji": "🔥",
            "category": "streak",
            "points": 300,
            "requirement": "30-day login streak"
        },
        "legend": {
            "name": "Legend",
            "description": "Logged in for 100 days straight",
            "emoji": "👑",
            "category": "streak",
            "points": 1000,
            "requirement": "100-day login streak"
        },
        
        # Premium Badges
        "supporter": {
            "name": "Supporter",
            "description": "Upgraded to premium subscription",
            "emoji": "💎",
            "category": "premium",
            "points": 100,
            "requirement": "Purchase any subscription"
        },
        "voice_lover": {
            "name": "Voice Lover",
            "description": "Generated 50 voice messages",
            "emoji": "🎵",
            "category": "premium",
            "points": 80,
            "requirement": "Generate 50 voice messages"
        },
        
        # Community Badges
        "community_member": {
            "name": "Community Member",
            "description": "Joined the Telegram community",
            "emoji": "🌐",
            "category": "community",
            "points": 25,
            "requirement": "Join Telegram community"
        },
        "helpful_member": {
            "name": "Helpful Member",
            "description": "Shared experience in community",
            "emoji": "🤝",
            "category": "community",
            "points": 35,
            "requirement": "Share community experience"
        },
        
        # Special Badges
        "early_adopter": {
            "name": "Early Adopter",
            "description": "One of the first 1000 users",
            "emoji": "🚀",
            "category": "special",
            "points": 150,
            "requirement": "Be among first 1000 users"
        },
        "mood_explorer": {
            "name": "Mood Explorer",
            "description": "Experienced all character moods",
            "emoji": "🎭",
            "category": "special",
            "points": 120,
            "requirement": "Experience all 6 character moods"
        }
    }
    
    # Level system
    LEVEL_THRESHOLDS = [
        0, 50, 150, 300, 500, 750, 1050, 1400, 1800, 2250,  # Levels 1-10
        2750, 3300, 3900, 4550, 5250, 6000, 6800, 7650, 8550, 9500,  # Levels 11-20
        10500, 11600, 12800, 14100, 15500, 17000, 18600, 20300, 22100, 24000  # Levels 21-30
    ]
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_gamification_data(self, user_id: int) -> Dict:
        """Get complete gamification data for user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Update login streak
        self._update_login_streak(user)
        
        # Get earned badges
        earned_badges = self._get_user_badges(user)
        
        # Calculate level and progress
        level_info = self._calculate_level_info(user.experience_points)
        
        # Get available achievements
        available_achievements = self._get_available_achievements(user)
        
        return {
            "user_id": user_id,
            "level": user.level,
            "experience_points": user.experience_points,
            "level_info": level_info,
            "login_streak": user.login_streak,
            "total_messages": user.total_messages_sent,
            "badges": {
                "earned": earned_badges,
                "total_earned": len(earned_badges),
                "total_available": len(self.BADGES)
            },
            "achievements": {
                "available": available_achievements,
                "next_milestone": self._get_next_milestone(user)
            },
            "stats": {
                "days_active": self._calculate_days_active(user),
                "favorite_category": self._get_favorite_character_category(user),
                "total_points_earned": user.experience_points
            }
        }
    
    def _update_login_streak(self, user: User):
        """Update user's login streak"""
        today = datetime.utcnow().date()
        last_login = user.last_login_date.date() if user.last_login_date else None
        
        if last_login == today:
            # Already logged in today
            return
        elif last_login == today - timedelta(days=1):
            # Consecutive day
            user.login_streak += 1
        elif last_login is None or last_login < today - timedelta(days=1):
            # Streak broken or first login
            user.login_streak = 1
        
        user.last_login_date = datetime.utcnow()
        self.db.commit()
    
    def _get_user_badges(self, user: User) -> List[Dict]:
        """Get list of badges earned by user"""
        if not user.badges_earned:
            return []
        
        try:
            badge_ids = json.loads(user.badges_earned) if isinstance(user.badges_earned, str) else user.badges_earned
        except:
            badge_ids = []
        
        earned_badges = []
        for badge_id in badge_ids:
            if badge_id in self.BADGES:
                badge = self.BADGES[badge_id].copy()
                badge["id"] = badge_id
                badge["earned_date"] = datetime.utcnow()  # In production, store actual earn date
                earned_badges.append(badge)
        
        return earned_badges
    
    def _calculate_level_info(self, experience_points: int) -> Dict:
        """Calculate user level and progress"""
        current_level = 1
        
        for level, threshold in enumerate(self.LEVEL_THRESHOLDS):
            if experience_points >= threshold:
                current_level = level + 1
            else:
                break
        
        # Calculate progress to next level
        if current_level <= len(self.LEVEL_THRESHOLDS):
            current_threshold = self.LEVEL_THRESHOLDS[current_level - 1]
            next_threshold = self.LEVEL_THRESHOLDS[current_level] if current_level < len(self.LEVEL_THRESHOLDS) else None
            
            if next_threshold:
                progress = experience_points - current_threshold
                required = next_threshold - current_threshold
                progress_percentage = (progress / required) * 100
            else:
                progress_percentage = 100
                required = 0
                progress = 0
        else:
            progress_percentage = 100
            required = 0
            progress = 0
        
        return {
            "current_level": current_level,
            "progress_percentage": round(progress_percentage, 1),
            "points_to_next_level": max(0, required - progress) if required > 0 else 0,
            "current_level_threshold": self.LEVEL_THRESHOLDS[current_level - 1] if current_level <= len(self.LEVEL_THRESHOLDS) else 0,
            "next_level_threshold": self.LEVEL_THRESHOLDS[current_level] if current_level < len(self.LEVEL_THRESHOLDS) else None
        }
    
    def _get_available_achievements(self, user: User) -> List[Dict]:
        """Get achievements user can work towards"""
        earned_badge_ids = []
        if user.badges_earned:
            try:
                earned_badge_ids = json.loads(user.badges_earned) if isinstance(user.badges_earned, str) else user.badges_earned
            except:
                earned_badge_ids = []
        
        available = []
        for badge_id, badge in self.BADGES.items():
            if badge_id not in earned_badge_ids:
                achievement = badge.copy()
                achievement["id"] = badge_id
                achievement["progress"] = self._calculate_badge_progress(user, badge_id)
                available.append(achievement)
        
        # Sort by progress (closest to completion first)
        available.sort(key=lambda x: x["progress"], reverse=True)
        return available[:10]  # Return top 10 closest achievements
    
    def _calculate_badge_progress(self, user: User, badge_id: str) -> float:
        """Calculate progress towards a specific badge"""
        if badge_id == "first_chat":
            return min(100, (user.total_messages_sent / 1) * 100)
        elif badge_id == "chatty":
            return min(100, (user.total_messages_sent / 100) * 100)
        elif badge_id == "conversation_master":
            return min(100, (user.total_messages_sent / 1000) * 100)
        elif badge_id == "daily_visitor":
            return min(100, (user.login_streak / 7) * 100)
        elif badge_id == "dedicated_user":
            return min(100, (user.login_streak / 30) * 100)
        elif badge_id == "legend":
            return min(100, (user.login_streak / 100) * 100)
        elif badge_id == "supporter":
            return 100 if user.is_premium else 0
        else:
            return 0  # Default for badges requiring special tracking
    
    def _get_next_milestone(self, user: User) -> Optional[Dict]:
        """Get the next achievement milestone"""
        available = self._get_available_achievements(user)
        if available:
            next_achievement = available[0]
            return {
                "badge": next_achievement,
                "progress": next_achievement["progress"],
                "points_reward": next_achievement["points"]
            }
        return None
    
    def award_badge(self, user_id: int, badge_id: str) -> Dict:
        """Award a badge to user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if badge_id not in self.BADGES:
            raise ValueError("Invalid badge ID")
        
        # Get current badges
        try:
            current_badges = json.loads(user.badges_earned) if user.badges_earned else []
        except:
            current_badges = []
        
        if badge_id in current_badges:
            return {
                "success": False,
                "message": "Badge already earned"
            }
        
        # Award badge
        current_badges.append(badge_id)
        user.badges_earned = json.dumps(current_badges)
        
        # Award experience points
        badge = self.BADGES[badge_id]
        user.experience_points += badge["points"]
        
        # Update level
        level_info = self._calculate_level_info(user.experience_points)
        old_level = user.level
        user.level = level_info["current_level"]
        
        self.db.commit()
        
        return {
            "success": True,
            "badge": badge,
            "points_earned": badge["points"],
            "total_points": user.experience_points,
            "level_up": user.level > old_level,
            "new_level": user.level
        }
    
    def add_experience_points(self, user_id: int, points: int, reason: str = "") -> Dict:
        """Add experience points to user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        old_level = user.level
        user.experience_points += points
        
        # Update level
        level_info = self._calculate_level_info(user.experience_points)
        user.level = level_info["current_level"]
        
        self.db.commit()
        
        return {
            "points_added": points,
            "total_points": user.experience_points,
            "level_up": user.level > old_level,
            "new_level": user.level,
            "reason": reason
        }
    
    def check_and_award_automatic_badges(self, user_id: int) -> List[Dict]:
        """Check and award badges that can be automatically earned"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        awarded_badges = []
        
        # Check message-based badges
        if user.total_messages_sent >= 1:
            result = self.award_badge(user_id, "first_chat")
            if result["success"]:
                awarded_badges.append(result)
        
        if user.total_messages_sent >= 100:
            result = self.award_badge(user_id, "chatty")
            if result["success"]:
                awarded_badges.append(result)
        
        if user.total_messages_sent >= 1000:
            result = self.award_badge(user_id, "conversation_master")
            if result["success"]:
                awarded_badges.append(result)
        
        # Check streak-based badges
        if user.login_streak >= 7:
            result = self.award_badge(user_id, "daily_visitor")
            if result["success"]:
                awarded_badges.append(result)
        
        if user.login_streak >= 30:
            result = self.award_badge(user_id, "dedicated_user")
            if result["success"]:
                awarded_badges.append(result)
        
        if user.login_streak >= 100:
            result = self.award_badge(user_id, "legend")
            if result["success"]:
                awarded_badges.append(result)
        
        # Check premium badges
        if user.is_premium:
            result = self.award_badge(user_id, "supporter")
            if result["success"]:
                awarded_badges.append(result)
        
        return awarded_badges
    
    def get_leaderboard(self, category: str = "points", limit: int = 10) -> List[Dict]:
        """Get leaderboard for different categories"""
        if category == "points":
            users = self.db.query(User).order_by(User.experience_points.desc()).limit(limit).all()
            return [
                {
                    "rank": i + 1,
                    "username": user.username,
                    "points": user.experience_points,
                    "level": user.level
                }
                for i, user in enumerate(users)
            ]
        elif category == "streak":
            users = self.db.query(User).order_by(User.login_streak.desc()).limit(limit).all()
            return [
                {
                    "rank": i + 1,
                    "username": user.username,
                    "streak": user.login_streak,
                    "level": user.level
                }
                for i, user in enumerate(users)
            ]
        elif category == "messages":
            users = self.db.query(User).order_by(User.total_messages_sent.desc()).limit(limit).all()
            return [
                {
                    "rank": i + 1,
                    "username": user.username,
                    "messages": user.total_messages_sent,
                    "level": user.level
                }
                for i, user in enumerate(users)
            ]
        
        return []
    
    def _calculate_days_active(self, user: User) -> int:
        """Calculate total days user has been active"""
        if not user.created_at:
            return 0
        
        days_since_signup = (datetime.utcnow() - user.created_at).days
        return max(1, days_since_signup)
    
    def _get_favorite_character_category(self, user: User) -> str:
        """Get user's favorite character category (mock implementation)"""
        # In production, analyze conversation history
        return "romantic"  # Default for now
    
    def get_all_badges(self) -> Dict:
        """Get information about all available badges"""
        badges_by_category = {}
        
        for badge_id, badge in self.BADGES.items():
            category = badge["category"]
            if category not in badges_by_category:
                badges_by_category[category] = []
            
            badge_info = badge.copy()
            badge_info["id"] = badge_id
            badges_by_category[category].append(badge_info)
        
        return {
            "badges_by_category": badges_by_category,
            "total_badges": len(self.BADGES),
            "categories": list(badges_by_category.keys())
        }
