#!/usr/bin/env python3
"""
Create a complete LiveRoom database with all 36 characters across 6 categories
"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.core.config import settings
from app.models.character import Character
from app.models.category import Category
from app.models.user import User
from app.services.character_service import CharacterPersonas

def clear_existing_data():
    """Clear existing data from tables"""
    print("🗑️  Clearing existing data...")

    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Delete in proper order to handle foreign key constraints
        # First delete messages, then conversations, then characters, categories, and users
        db.execute(text("DELETE FROM messages"))
        db.execute(text("DELETE FROM conversations"))
        db.execute(text("DELETE FROM characters"))
        db.execute(text("DELETE FROM categories"))
        db.execute(text("DELETE FROM users"))
        db.commit()
        print("✅ Existing data cleared successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error clearing data: {e}")
        raise
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    print("📋 Creating database tables...")
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def create_categories():
    """Create all 6 categories"""
    print("📂 Creating categories...")
    
    categories_data = [
        {
            "name": "romantic_companions",
            "description": "Romantic Companions (6)",
            "display_name": "💕 Romantic Companions",
            "sort_order": 1
        },
        {
            "name": "flirty_chat", 
            "description": "Flirty Chat (6)",
            "display_name": "😘 Flirty Chat",
            "sort_order": 2
        },
        {
            "name": "mood_boosters",
            "description": "Mood Boosters (6)", 
            "display_name": "🌟 Mood Boosters",
            "sort_order": 3
        },
        {
            "name": "fantasy_roleplay",
            "description": "Fantasy Roleplay (6)",
            "display_name": "🧙‍♀️ Fantasy Roleplay", 
            "sort_order": 4
        },
        {
            "name": "intimate_conversations",
            "description": "Intimate Conversations (6)",
            "display_name": "💋 Intimate Conversations",
            "sort_order": 5
        },
        {
            "name": "entertainment_fun",
            "description": "Entertainment & Fun (6)",
            "display_name": "🎭 Entertainment & Fun",
            "sort_order": 6
        }
    ]
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        for cat_data in categories_data:
            category = Category(
                name=cat_data["name"],
                description=cat_data["description"],
                is_active=True,
                sort_order=cat_data["sort_order"],
                category_type="general"
            )
            db.add(category)
        
        db.commit()
        print("✅ Categories created successfully!")
        
        # Return category mapping
        categories = db.query(Category).all()
        category_map = {cat.name: cat.id for cat in categories}
        return category_map
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating categories: {e}")
        raise
    finally:
        db.close()

def create_demo_user():
    """Create a demo user for testing"""
    print("👤 Creating demo user...")

    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        demo_user = User(
            id=1,
            username="demo_user",
            email="demo@liveroom.ai",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        print("✅ Demo user created successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating demo user: {e}")
        raise
    finally:
        db.close()

def create_all_characters(category_map):
    """Create all 36 characters"""
    print("👥 Creating all 36 characters...")
    
    # Character mapping by category (using actual available personas)
    character_categories = {
        # Romantic Companions (6)
        "luna": "romantic_companions",
        "valentina": "romantic_companions",
        "scarlett": "romantic_companions",
        "elena": "romantic_companions",
        "aurora": "romantic_companions",
        "victoria": "romantic_companions",

        # Flirty Chat (6)
        "sophia": "flirty_chat",
        "maya": "flirty_chat",
        "chloe": "flirty_chat",
        "jasmine": "flirty_chat",
        "riley": "flirty_chat",
        "amber": "flirty_chat",

        # Mood Boosters (6)
        "aria": "mood_boosters",
        "sunny": "mood_boosters",
        "joy": "mood_boosters",
        "bliss": "mood_boosters",
        "spark": "mood_boosters",
        "hope": "mood_boosters",

        # Fantasy Roleplay (6)
        "isabella": "fantasy_roleplay",
        "seraphina": "fantasy_roleplay",
        "luna_wolf": "fantasy_roleplay",
        "morgana": "fantasy_roleplay",
        "celeste": "fantasy_roleplay",
        "nyx": "fantasy_roleplay",

        # Intimate Conversations (6)
        "zara": "intimate_conversations",
        "diana": "intimate_conversations",
        "ruby": "intimate_conversations",
        "eva": "intimate_conversations",
        "phoenix": "intimate_conversations",
        "velvet": "intimate_conversations",

        # Entertainment & Fun (6)
        "astro_baba": "entertainment_fun",
        "jester": "entertainment_fun",
        "melody": "entertainment_fun",
        "nova": "entertainment_fun",
        "pixel": "entertainment_fun",
        "sage": "entertainment_fun"
    }
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        created_count = 0
        all_personas = CharacterPersonas.get_all_personas()
        
        for character_key, category_name in character_categories.items():
            if character_key in all_personas:
                persona = all_personas[character_key]
                category_id = category_map[category_name]
                
                character = Character(
                    name=persona["name"],
                    display_name=persona["display_name"],
                    description=persona["description"],
                    personality=persona["personality"],
                    system_prompt=persona["system_prompt"],
                    traits=persona["traits"],
                    conversation_style=persona["conversation_style"],
                    age_range=persona["age_range"],
                    background_story=persona["background_story"],
                    category_id=category_id,
                    avatar_urls=[f"/avatars/{character_key}.jpg"],
                    is_active=True
                )
                
                db.add(character)
                created_count += 1
                print(f"  ✓ Created {persona['display_name']}")
            else:
                print(f"  ⚠️  Persona '{character_key}' not found in CharacterPersonas")
        
        db.commit()
        print(f"✅ Successfully created {created_count} characters!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating characters: {e}")
        raise
    finally:
        db.close()

def verify_database():
    """Verify the database was created correctly"""
    print("🔍 Verifying database...")
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Count categories
        category_count = db.query(Category).count()
        print(f"📂 Categories: {category_count}")
        
        # Count characters
        character_count = db.query(Character).count()
        print(f"👥 Characters: {character_count}")
        
        # Count by category
        categories = db.query(Category).all()
        for category in categories:
            char_count = db.query(Character).filter(Character.category_id == category.id).count()
            print(f"  {category.description}: {char_count} characters")
        
        if category_count == 6 and character_count == 36:
            print("✅ Database verification successful!")
            return True
        else:
            print("❌ Database verification failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False
    finally:
        db.close()

def main():
    """Main function to create the complete database"""
    print("🚀 Creating complete LiveRoom database with 36 characters...")
    print("=" * 60)

    try:
        # Step 1: Clear existing data
        clear_existing_data()

        # Step 2: Create tables
        create_tables()

        # Step 3: Create demo user
        create_demo_user()

        # Step 4: Create categories
        category_map = create_categories()

        # Step 5: Create all characters
        create_all_characters(category_map)

        # Step 6: Verify everything
        if verify_database():
            print("=" * 60)
            print("🎉 SUCCESS! Complete LiveRoom database created!")
            print("📊 Database contains:")
            print("   • 6 Categories")
            print("   • 36 Characters (6 per category)")
            print("   • All characters are active and ready for chat")
            print("=" * 60)
        else:
            print("❌ Database creation completed but verification failed!")

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
