from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    personality = Column(Text)  # Detailed personality description
    system_prompt = Column(Text)  # OpenAI system prompt
    avatar_urls = Column(JSON)  # List of avatar image URLs
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    
    # Character traits
    traits = Column(JSON)  # {"flirty": 8, "romantic": 9, "playful": 7}
    conversation_style = Column(String(50))  # casual, formal, flirty, romantic
    age_range = Column(String(20))  # "20-25", "25-30", etc.
    background_story = Column(Text)
    
    # Relationships
    category = relationship("Category", back_populates="characters")
    subcategory = relationship("Subcategory", back_populates="characters")
    conversations = relationship("Conversation", back_populates="character")
    messages = relationship("Message", back_populates="character")
