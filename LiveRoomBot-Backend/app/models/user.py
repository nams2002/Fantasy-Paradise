from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class SubscriptionPlan(enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Made nullable for Telegram users
    telegram_id = Column(String(50), unique=True, index=True, nullable=True)  # For Telegram integration
    is_active = Column(Boolean, default=True)

    # Subscription Management
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    subscription_start_date = Column(DateTime(timezone=True), nullable=True)
    subscription_end_date = Column(DateTime(timezone=True), nullable=True)
    is_premium = Column(Boolean, default=False)

    # Usage Tracking
    messages_used_today = Column(Integer, default=0)
    images_generated_today = Column(Integer, default=0)
    last_reset_date = Column(DateTime(timezone=True), server_default=func.now())
    total_messages_sent = Column(Integer, default=0)

    # Gamification
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    login_streak = Column(Integer, default=0)
    last_login_date = Column(DateTime(timezone=True), nullable=True)
    badges_earned = Column(String(1000), default="")  # JSON string of badge IDs

    # Payment
    upi_id = Column(String(100), nullable=True)
    last_payment_date = Column(DateTime(timezone=True), nullable=True)
    total_spent = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    messages = relationship("Message", back_populates="user")
