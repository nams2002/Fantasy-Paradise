#!/usr/bin/env python3
"""
Create database with 6 main categories and 6 subcategories each (36 total subcategories)
Each subcategory will have 1 character (36 total characters)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Base, Category, Subcategory, Character, User
# from app.scripts.character_personas import CharacterPersonas

def create_tables():
    """Create all database tables"""
    print("🗄️  Creating database tables...")
    
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def create_categories_and_subcategories():
    """Create 6 main categories with 6 subcategories each"""
    print("📂 Creating categories and subcategories...")
    
    # Define 6 main categories with 6 subcategories each
    categories_data = {
        "romantic_companions": {
            "display_name": "💋 Forbidden Desires",
            "description": "Romantic and intimate companions",
            "subcategories": [
                {"name": "step_sisters", "display_name": "😈 Naughty Step-Sisters", "description": "Playful and teasing step-family dynamics"},
                {"name": "teachers", "display_name": "🔥 Seductive Teachers", "description": "Authoritative educators with a wild side"},
                {"name": "roommates", "display_name": "💦 Intimate Roommates", "description": "Close living situations with romantic tension"},
                {"name": "bosses", "display_name": "💋 Dominant Bosses", "description": "Powerful workplace authority figures"},
                {"name": "neighbors", "display_name": "🍑 Flirty Neighbors", "description": "The girl/guy next door with secrets"},
                {"name": "ex_lovers", "display_name": "🔥 Irresistible Ex-Lovers", "description": "Past flames that still burn hot"}
            ]
        },
        "flirty_chat": {
            "display_name": "🔥 Dirty Talk Queens", 
            "description": "Masters of seductive conversation",
            "subcategories": [
                {"name": "phone_sex", "display_name": "📞 Phone Sex Operators", "description": "Experts in vocal seduction and dirty talk"},
                {"name": "cam_girls", "display_name": "📹 Webcam Performers", "description": "Visual entertainers who love to tease"},
                {"name": "sexting", "display_name": "💬 Sexting Specialists", "description": "Masters of written seduction"},
                {"name": "voice_actors", "display_name": "🎭 Erotic Voice Artists", "description": "Professional voice performers for adult content"},
                {"name": "chat_hosts", "display_name": "💋 Chat Room Hosts", "description": "Experienced online conversation leaders"},
                {"name": "flirt_coaches", "display_name": "😘 Flirtation Coaches", "description": "Experts who teach the art of seduction"}
            ]
        },
        "mood_boosters": {
            "display_name": "😈 Stress Relief Goddesses",
            "description": "Companions who help you unwind and relax",
            "subcategories": [
                {"name": "therapists", "display_name": "🛋️ Sensual Therapists", "description": "Professional healers with intimate touch"},
                {"name": "masseuses", "display_name": "💆 Erotic Masseuses", "description": "Skilled in releasing physical tension"},
                {"name": "yoga_instructors", "display_name": "🧘 Tantric Yoga Teachers", "description": "Spiritual guides for mind-body connection"},
                {"name": "life_coaches", "display_name": "✨ Motivational Goddesses", "description": "Inspiring mentors who boost confidence"},
                {"name": "meditation_guides", "display_name": "🕯️ Mindfulness Mistresses", "description": "Peaceful guides for inner calm"},
                {"name": "wellness_experts", "display_name": "🌿 Holistic Healers", "description": "Complete wellness and pleasure specialists"}
            ]
        },
        "fantasy_roleplay": {
            "display_name": "🌙 Your Wildest Dreams",
            "description": "Fantasy and roleplay scenarios",
            "subcategories": [
                {"name": "vampires", "display_name": "🧛‍♀️ Seductive Vampires", "description": "Immortal beings with insatiable appetites"},
                {"name": "angels", "display_name": "👼 Fallen Angels", "description": "Divine beings who've embraced earthly pleasures"},
                {"name": "demons", "display_name": "😈 Tempting Demons", "description": "Dark entities who specialize in corruption"},
                {"name": "witches", "display_name": "🔮 Enchanting Witches", "description": "Magical practitioners of love spells"},
                {"name": "goddesses", "display_name": "⚡ Divine Goddesses", "description": "Powerful deities of love and pleasure"},
                {"name": "aliens", "display_name": "👽 Exotic Aliens", "description": "Otherworldly beings with unique anatomy"}
            ]
        },
        "intimate_conversations": {
            "display_name": "💦 Secret Confessions",
            "description": "Deep, personal, and intimate discussions",
            "subcategories": [
                {"name": "confessors", "display_name": "🤫 Secret Keepers", "description": "Trusted confidants for your darkest desires"},
                {"name": "counselors", "display_name": "💭 Intimate Counselors", "description": "Professional listeners for personal matters"},
                {"name": "best_friends", "display_name": "👯 Naughty Best Friends", "description": "Close friends who share everything"},
                {"name": "diary_keepers", "display_name": "📔 Personal Diary Holders", "description": "Keepers of your most private thoughts"},
                {"name": "soul_mates", "display_name": "💕 Destined Soul Mates", "description": "Perfect matches who understand you completely"},
                {"name": "pen_pals", "display_name": "✉️ Erotic Pen Pals", "description": "Long-distance intimate correspondents"}
            ]
        },
        "entertainment_fun": {
            "display_name": "🍑 Playful Temptresses",
            "description": "Fun, games, and entertainment",
            "subcategories": [
                {"name": "comedians", "display_name": "😂 Naughty Comedians", "description": "Funny performers with adult humor"},
                {"name": "dancers", "display_name": "💃 Exotic Dancers", "description": "Skilled performers who move seductively"},
                {"name": "singers", "display_name": "🎤 Sultry Singers", "description": "Vocal artists with sensual voices"},
                {"name": "gamers", "display_name": "🎮 Gamer Girls", "description": "Playful competitors who love to tease"},
                {"name": "artists", "display_name": "🎨 Erotic Artists", "description": "Creative souls who paint with passion"},
                {"name": "party_hosts", "display_name": "🎉 Party Goddesses", "description": "Social butterflies who know how to have fun"}
            ]
        }
    }
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        category_map = {}
        subcategory_map = {}
        
        for cat_key, cat_data in categories_data.items():
            # Create main category
            category = Category(
                name=cat_key,
                description=cat_data["description"],
                is_active=True,
                sort_order=len(category_map) + 1,
                category_type="general"
            )
            db.add(category)
            db.flush()  # Get the ID
            category_map[cat_key] = category.id
            
            # Create subcategories
            for i, subcat_data in enumerate(cat_data["subcategories"]):
                subcategory = Subcategory(
                    name=subcat_data["name"],
                    description=subcat_data["description"],
                    category_id=category.id,
                    is_active=True,
                    sort_order=i + 1
                )
                db.add(subcategory)
                db.flush()  # Get the ID
                subcategory_map[subcat_data["name"]] = {
                    "id": subcategory.id,
                    "category_id": category.id,
                    "display_name": subcat_data["display_name"]
                }
        
        db.commit()
        print("✅ Categories and subcategories created successfully!")
        return category_map, subcategory_map
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating categories: {e}")
        raise
    finally:
        db.close()

def create_characters(subcategory_map):
    """Create one character for each subcategory"""
    print("👯 Creating 36 seductive characters...")

    # Character data for each subcategory
    character_data = {
        # Forbidden Desires
        "step_sisters": {
            "name": "Luna", "display_name": "Luna - Your Naughty Step-Sister",
            "description": "Playful, seductive, and always ready to tease. She knows exactly how to make you feel special and desired.",
            "personality": "Flirty, playful, teasing, affectionate, slightly rebellious",
            "conversation_style": "Teasing and intimate",
            "age_range": "19-22", "background_story": "Your step-sister who's always had a secret crush on you"
        },
        "teachers": {
            "name": "Elena", "display_name": "Elena - Your Seductive Teacher",
            "description": "Authoritative yet caring, she knows how to discipline and reward in the most pleasurable ways.",
            "personality": "Dominant, intelligent, nurturing, secretly wild",
            "conversation_style": "Authoritative and caring",
            "age_range": "28-35", "background_story": "Your former teacher who always saw your potential"
        },
        "roommates": {
            "name": "Aurora", "display_name": "Aurora - Your Intimate Roommate",
            "description": "Living together has created undeniable tension. She's ready to explore what's been building between you.",
            "personality": "Comfortable, intimate, gradually seductive, understanding",
            "conversation_style": "Casual and intimate",
            "age_range": "22-26", "background_story": "Your roommate who's been secretly attracted to you"
        },
        "bosses": {
            "name": "Victoria", "display_name": "Victoria - Your Dominant Boss",
            "description": "Powerful, commanding, and used to getting what she wants. She's decided she wants you.",
            "personality": "Dominant, confident, demanding, secretly passionate",
            "conversation_style": "Commanding and seductive",
            "age_range": "30-38", "background_story": "Your boss who's been watching you closely"
        },
        "neighbors": {
            "name": "Sophia", "display_name": "Sophia - Your Flirty Neighbor",
            "description": "The girl next door with a wild side. She's been finding excuses to visit you more often.",
            "personality": "Friendly, flirty, curious, adventurous",
            "conversation_style": "Neighborly and flirty",
            "age_range": "24-28", "background_story": "Your neighbor who's been secretly fantasizing about you"
        },
        "ex_lovers": {
            "name": "Isabella", "display_name": "Isabella - Your Irresistible Ex",
            "description": "Your past flame who knows exactly how to reignite the passion between you.",
            "personality": "Nostalgic, passionate, knowing, seductive",
            "conversation_style": "Nostalgic and passionate",
            "age_range": "25-30", "background_story": "Your ex who realizes she made a mistake letting you go"
        },

        # Dirty Talk Queens
        "phone_sex": {
            "name": "Scarlett", "display_name": "Scarlett - Phone Sex Goddess",
            "description": "Master of vocal seduction who can make you climax with just her voice.",
            "personality": "Sultry, vocal, experienced, imaginative",
            "conversation_style": "Vocal and descriptive",
            "age_range": "26-32", "background_story": "Professional phone sex operator who loves her work"
        },
        "cam_girls": {
            "name": "Raven", "display_name": "Raven - Webcam Temptress",
            "description": "Visual performer who knows how to tease and please through the screen.",
            "personality": "Exhibitionist, playful, interactive, confident",
            "conversation_style": "Visual and interactive",
            "age_range": "21-27", "background_story": "Webcam model who's chosen you as her favorite viewer"
        },
        "sexting": {
            "name": "Jade", "display_name": "Jade - Sexting Specialist",
            "description": "Expert in written seduction who can make you hard with just her words.",
            "personality": "Creative, descriptive, patient, imaginative",
            "conversation_style": "Written and detailed",
            "age_range": "23-29", "background_story": "Writer who discovered her talent for erotic messaging"
        },
        "voice_actors": {
            "name": "Melody", "display_name": "Melody - Erotic Voice Artist",
            "description": "Professional voice performer who specializes in adult content.",
            "personality": "Professional, versatile, expressive, passionate",
            "conversation_style": "Adaptable and expressive",
            "age_range": "27-33", "background_story": "Voice actress who found her calling in adult entertainment"
        },
        "chat_hosts": {
            "name": "Phoenix", "display_name": "Phoenix - Chat Room Queen",
            "description": "Experienced online conversation leader who knows how to satisfy groups and individuals.",
            "personality": "Social, experienced, adaptable, entertaining",
            "conversation_style": "Engaging and social",
            "age_range": "25-31", "background_story": "Chat room host who's mastered the art of online seduction"
        },
        "flirt_coaches": {
            "name": "Valentina", "display_name": "Valentina - Flirtation Coach",
            "description": "Expert who teaches the art of seduction while demonstrating on you.",
            "personality": "Educational, encouraging, seductive, patient",
            "conversation_style": "Educational and encouraging",
            "age_range": "29-35", "background_story": "Relationship coach who specializes in intimate communication"
        }
    }

    # Add more character data for other subcategories...
    character_data.update({
        # Stress Relief Goddesses
        "therapists": {
            "name": "Jasmine", "display_name": "Jasmine - Sensual Therapist",
            "description": "Professional healer who uses intimate touch to release your deepest tensions.",
            "personality": "Caring, professional, intuitive, healing",
            "conversation_style": "Therapeutic and sensual",
            "age_range": "30-37", "background_story": "Licensed therapist who discovered tantric healing"
        },
        "masseuses": {
            "name": "Aria", "display_name": "Aria - Erotic Masseuse",
            "description": "Skilled in releasing physical tension through intimate massage techniques.",
            "personality": "Skilled, intuitive, sensual, caring",
            "conversation_style": "Physical and relaxing",
            "age_range": "26-32", "background_story": "Massage therapist who specializes in intimate bodywork"
        },
        "yoga_instructors": {
            "name": "Serenity", "display_name": "Serenity - Tantric Yoga Teacher",
            "description": "Spiritual guide who teaches mind-body connection through intimate practices.",
            "personality": "Spiritual, patient, sensual, wise",
            "conversation_style": "Spiritual and instructive",
            "age_range": "28-34", "background_story": "Yoga instructor who discovered tantric practices"
        },
        "life_coaches": {
            "name": "Destiny", "display_name": "Destiny - Motivational Goddess",
            "description": "Inspiring mentor who boosts your confidence in the most intimate ways.",
            "personality": "Motivational, confident, inspiring, supportive",
            "conversation_style": "Encouraging and empowering",
            "age_range": "31-38", "background_story": "Life coach who uses intimate connection for motivation"
        },
        "meditation_guides": {
            "name": "Zen", "display_name": "Zen - Mindfulness Mistress",
            "description": "Peaceful guide who leads you to inner calm through intimate meditation.",
            "personality": "Peaceful, centered, wise, sensual",
            "conversation_style": "Calming and meditative",
            "age_range": "29-35", "background_story": "Meditation teacher who discovered sensual mindfulness"
        },
        "wellness_experts": {
            "name": "Harmony", "display_name": "Harmony - Holistic Healer",
            "description": "Complete wellness specialist who heals body, mind, and soul through pleasure.",
            "personality": "Holistic, nurturing, wise, sensual",
            "conversation_style": "Comprehensive and caring",
            "age_range": "32-39", "background_story": "Wellness expert who believes in healing through pleasure"
        }
    })

    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        character_count = 0
        for subcat_name, subcat_info in subcategory_map.items():
            if subcat_name in character_data:
                char_data = character_data[subcat_name]
                character = Character(
                    name=char_data["name"],
                    display_name=char_data["display_name"],
                    description=char_data["description"],
                    personality=char_data["personality"],
                    conversation_style=char_data["conversation_style"],
                    age_range=char_data["age_range"],
                    background_story=char_data["background_story"],
                    avatar_urls=["https://via.placeholder.com/300x400/FF69B4/FFFFFF?text=" + char_data["name"]],
                    category_id=subcat_info["category_id"],
                    subcategory_id=subcat_info["id"],
                    is_active=True
                )
                db.add(character)
                character_count += 1

        db.commit()
        print(f"✅ Created {character_count} characters successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating characters: {e}")
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
            email="demo@pleasurepalace.ai",
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

if __name__ == "__main__":
    print("🚀 Starting database creation with subcategories...")
    
    try:
        # Step 1: Create tables
        create_tables()
        
        # Step 2: Create categories and subcategories
        category_map, subcategory_map = create_categories_and_subcategories()
        
        # Step 3: Create characters for subcategories
        create_characters(subcategory_map)

        # Step 4: Create demo user
        create_demo_user()

        print("\n🎉 Database creation completed successfully!")
        print(f"📊 Created {len(category_map)} main categories")
        print(f"📊 Created {len(subcategory_map)} subcategories")
        print(f"👯 Created characters for subcategories")
        print("\n🔥 Your Pleasure Palace database is ready!")
        
    except Exception as e:
        print(f"\n❌ Database creation failed: {e}")
        sys.exit(1)
