from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models.user import User, SubscriptionPlan
from app.core.database import get_db
import json

class SubscriptionService:
    """Service for managing user subscriptions and usage limits"""
    
    # Subscription Plans Configuration
    PLANS = {
        SubscriptionPlan.FREE: {
            "name": "Free Plan",
            "price": 0,
            "currency": "INR",
            "messages_per_day": 20,  # Reduced to create urgency
            "images_per_day": 0,
            "voice_messages": False,
            "premium_characters": False,
            "features": ["20 messages/day", "6 basic characters", "Community access"]
        },
        SubscriptionPlan.BASIC: {
            "name": "Basic Plan",
            "price": 199,  # Optimized pricing
            "currency": "INR",
            "messages_per_day": -1,  # Unlimited
            "images_per_day": 5,  # Increased value
            "voice_messages": True,
            "premium_characters": False,
            "features": ["Unlimited messages", "5 images/day", "Voice messages", "All basic characters", "Priority support"]
        },
        SubscriptionPlan.PRO: {
            "name": "Pro Plan",
            "price": 499,  # More accessible pricing
            "currency": "INR",
            "messages_per_day": -1,  # Unlimited
            "images_per_day": 15,  # Increased value
            "voice_messages": True,
            "premium_characters": True,
            "features": ["Unlimited messages", "15 images/day", "Voice messages", "Premium characters", "Custom characters", "Priority support", "Advanced features"]
        }
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_plan_info(self, user_id: int) -> Dict:
        """Get user's current subscription plan information"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Check if subscription is still valid
        if user.subscription_end_date and user.subscription_end_date < datetime.utcnow():
            # Subscription expired, downgrade to free
            user.subscription_plan = SubscriptionPlan.FREE
            user.is_premium = False
            self.db.commit()
        
        plan_info = self.PLANS[user.subscription_plan].copy()
        plan_info.update({
            "current_plan": user.subscription_plan.value,
            "subscription_start": user.subscription_start_date,
            "subscription_end": user.subscription_end_date,
            "is_active": self._is_subscription_active(user),
            "messages_used_today": user.messages_used_today,
            "images_generated_today": user.images_generated_today,
            "can_send_message": self._can_send_message(user),
            "can_generate_image": self._can_generate_image(user),
            "days_remaining": self._get_days_remaining(user)
        })
        
        return plan_info
    
    def _is_subscription_active(self, user: User) -> bool:
        """Check if user's subscription is currently active"""
        if user.subscription_plan == SubscriptionPlan.FREE:
            return True
        
        if not user.subscription_end_date:
            return False
            
        return user.subscription_end_date > datetime.utcnow()
    
    def _get_days_remaining(self, user: User) -> Optional[int]:
        """Get days remaining in subscription"""
        if user.subscription_plan == SubscriptionPlan.FREE or not user.subscription_end_date:
            return None
            
        remaining = user.subscription_end_date - datetime.utcnow()
        return max(0, remaining.days)
    
    def _can_send_message(self, user: User) -> bool:
        """Check if user can send a message"""
        self._reset_daily_usage_if_needed(user)
        
        plan = self.PLANS[user.subscription_plan]
        if plan["messages_per_day"] == -1:  # Unlimited
            return True
            
        return user.messages_used_today < plan["messages_per_day"]
    
    def _can_generate_image(self, user: User) -> bool:
        """Check if user can generate an image"""
        self._reset_daily_usage_if_needed(user)
        
        plan = self.PLANS[user.subscription_plan]
        if plan["images_per_day"] == 0:  # Not allowed
            return False
            
        if plan["images_per_day"] == -1:  # Unlimited
            return True
            
        return user.images_generated_today < plan["images_per_day"]
    
    def _reset_daily_usage_if_needed(self, user: User):
        """Reset daily usage counters if it's a new day"""
        today = datetime.utcnow().date()
        last_reset = user.last_reset_date.date() if user.last_reset_date else None
        
        if last_reset != today:
            user.messages_used_today = 0
            user.images_generated_today = 0
            user.last_reset_date = datetime.utcnow()
            self.db.commit()
    
    def increment_message_usage(self, user_id: int) -> bool:
        """Increment user's message usage and return if successful"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        if not self._can_send_message(user):
            return False
        
        user.messages_used_today += 1
        user.total_messages_sent += 1
        self.db.commit()
        return True
    
    def increment_image_usage(self, user_id: int) -> bool:
        """Increment user's image generation usage and return if successful"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        if not self._can_generate_image(user):
            return False
        
        user.images_generated_today += 1
        self.db.commit()
        return True
    
    def upgrade_subscription(self, user_id: int, plan: SubscriptionPlan, payment_id: str) -> Dict:
        """Upgrade user's subscription plan"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if plan == SubscriptionPlan.FREE:
            raise ValueError("Cannot upgrade to free plan")
        
        # Set subscription details
        user.subscription_plan = plan
        user.subscription_start_date = datetime.utcnow()
        user.subscription_end_date = datetime.utcnow() + timedelta(days=30)  # 30-day subscription
        user.is_premium = plan in [SubscriptionPlan.BASIC, SubscriptionPlan.PRO]
        user.last_payment_date = datetime.utcnow()
        user.total_spent += self.PLANS[plan]["price"]
        
        # Reset usage counters
        user.messages_used_today = 0
        user.images_generated_today = 0
        user.last_reset_date = datetime.utcnow()
        
        self.db.commit()
        
        return {
            "success": True,
            "message": f"Successfully upgraded to {self.PLANS[plan]['name']}",
            "plan": plan.value,
            "expires_on": user.subscription_end_date,
            "payment_id": payment_id
        }
    
    def get_all_plans(self) -> Dict:
        """Get information about all available plans"""
        return {
            "plans": [
                {
                    "id": plan.value,
                    "name": info["name"],
                    "price": info["price"],
                    "currency": info["currency"],
                    "features": info["features"],
                    "messages_per_day": "Unlimited" if info["messages_per_day"] == -1 else info["messages_per_day"],
                    "images_per_day": info["images_per_day"],
                    "voice_messages": info["voice_messages"],
                    "premium_characters": info["premium_characters"]
                }
                for plan, info in self.PLANS.items()
            ]
        }
    
    def check_usage_limits(self, user_id: int) -> Dict:
        """Check user's current usage against their limits"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        self._reset_daily_usage_if_needed(user)
        plan = self.PLANS[user.subscription_plan]
        
        return {
            "plan": user.subscription_plan.value,
            "messages": {
                "used": user.messages_used_today,
                "limit": "Unlimited" if plan["messages_per_day"] == -1 else plan["messages_per_day"],
                "can_send": self._can_send_message(user)
            },
            "images": {
                "used": user.images_generated_today,
                "limit": plan["images_per_day"],
                "can_generate": self._can_generate_image(user)
            },
            "features": {
                "voice_messages": plan["voice_messages"],
                "premium_characters": plan["premium_characters"]
            }
        }
    
    def get_subscription_stats(self) -> Dict:
        """Get overall subscription statistics"""
        total_users = self.db.query(User).count()
        free_users = self.db.query(User).filter(User.subscription_plan == SubscriptionPlan.FREE).count()
        basic_users = self.db.query(User).filter(User.subscription_plan == SubscriptionPlan.BASIC).count()
        pro_users = self.db.query(User).filter(User.subscription_plan == SubscriptionPlan.PRO).count()
        
        # Calculate revenue (approximate)
        total_revenue = (basic_users * 100) + (pro_users * 1000)
        
        return {
            "total_users": total_users,
            "free_users": free_users,
            "basic_users": basic_users,
            "pro_users": pro_users,
            "conversion_rate": round((basic_users + pro_users) / total_users * 100, 2) if total_users > 0 else 0,
            "estimated_monthly_revenue": total_revenue
        }
