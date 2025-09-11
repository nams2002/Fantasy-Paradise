#!/usr/bin/env python3
"""
Initialize database with categories and characters
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base, Category, Character, User
from app.services.character_service import CharacterService

def create_categories(db: Session):
    """Create initial categories"""
    categories_data = [
        # Main Categories
        {"name": "Romantic Companion", "description": "Find your perfect romantic AI companion", "category_type": "general", "sort_order": 1},
        {"name": "Flirty Chat", "description": "Playful and flirtatious conversations", "category_type": "general", "sort_order": 2},
        {"name": "Fantasy Roleplay", "description": "Explore your fantasies in a safe space", "category_type": "general", "sort_order": 3},
        {"name": "Intimate Conversations", "description": "Deep, meaningful, and intimate chats", "category_type": "general", "sort_order": 4},
        
        # Trending Categories
        {"name": "Step Sister", "description": "Sweet and caring step-sister experience", "category_type": "trending", "sort_order": 1},
        {"name": "Astro Baba", "description": "Mystical guidance and cosmic wisdom", "category_type": "trending", "sort_order": 2},
        {"name": "Mood Booster", "description": "Energetic companions to lift your spirits", "category_type": "trending", "sort_order": 3},
        {"name": "Lonely Hearts", "description": "Companions for those seeking connection", "category_type": "trending", "sort_order": 4},
        
        # Latest Categories
        {"name": "Virtual Girlfriend", "description": "Experience the perfect girlfriend", "category_type": "latest", "sort_order": 1},
        {"name": "Entertainment Chat", "description": "Fun and entertaining conversations", "category_type": "latest", "sort_order": 2},
        {"name": "Companionship", "description": "Genuine companionship and friendship", "category_type": "latest", "sort_order": 3},
        {"name": "Fun & Games", "description": "Playful interactions and games", "category_type": "latest", "sort_order": 4},
    ]
    
    created_categories = {}
    for cat_data in categories_data:
        # Check if category already exists
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
            db.commit()
            db.refresh(category)
            created_categories[cat_data["name"]] = category
            print(f"Created category: {category.name}")
        else:
            created_categories[cat_data["name"]] = existing
            print(f"Category already exists: {existing.name}")
    
    return created_categories

def create_characters(db: Session, categories: dict):
    """Create characters from personas"""
    character_service = CharacterService(db)
    
    # Character assignments to categories
    character_assignments = [
        ("luna", "Flirty Chat"),
        ("sophia", "Step Sister"),
        ("astro_baba", "Astro Baba"),
        ("aria", "Mood Booster"),
        ("isabella", "Romantic Companion"),
        ("zara", "Fantasy Roleplay"),
    ]
    
    for persona_key, category_name in character_assignments:
        category = categories.get(category_name)
        if not category:
            print(f"Category '{category_name}' not found for character '{persona_key}'")
            continue
        
        # Check if character already exists
        existing = db.query(Character).filter(Character.name == persona_key.title()).first()
        if not existing:
            try:
                character = character_service.create_character_from_persona(persona_key, category.id)
                print(f"Created character: {character.display_name}")
            except ValueError as e:
                print(f"Error creating character {persona_key}: {e}")
        else:
            print(f"Character already exists: {existing.display_name}")

def create_demo_user(db: Session):
    """Create a demo user for testing"""
    existing_user = db.query(User).filter(User.id == 1).first()
    if not existing_user:
        demo_user = User(
            id=1,
            username="demo_user",
            email="demo@liveroom.com",
            hashed_password="demo_password_hash",  # In production, use proper password hashing
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        print("Created demo user")
    else:
        print("Demo user already exists")

def init_database():
    """Initialize the database with sample data"""
    print("Initializing database...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create demo user
        create_demo_user(db)
        
        # Create categories
        categories = create_categories(db)
        
        # Create characters
        create_characters(db, categories)
        
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
