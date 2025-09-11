from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    image_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    category_type = Column(String(50), default="general")  # general, trending, latest
    
    # Relationships
    characters = relationship("Character", back_populates="category")
    subcategories = relationship("Subcategory", back_populates="category")
