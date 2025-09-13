#!/usr/bin/env python3
"""
Initialize database with categories and characters
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base, Category, Character, Subcategory, User
from app.services.character_service import CharacterService, CharacterPersonas

def create_categories(db: Session):
    """Create main UI categories (6 groups)"""
    categories_data = [
        {"name": "Forbidden Desires", "description": "Seductive companions who push your boundaries.", "category_type": "general", "sort_order": 1},
        {"name": "Dirty Talk Queens", "description": "Masters of flirtation and irresistible chat.", "category_type": "general", "sort_order": 2},
        {"name": "Stress Relief Goddesses", "description": "Healing, calming and uplifting companions.", "category_type": "general", "sort_order": 3},
        {"name": "Your Wildest Dreams", "description": "Fantasy roleplay with supernatural allure.", "category_type": "general", "sort_order": 4},
        {"name": "Secret Confessions", "description": "Deep, intimate and emotionally connected.", "category_type": "general", "sort_order": 5},
        {"name": "Playful Temptresses", "description": "Entertainment and fun-loving companions.", "category_type": "general", "sort_order": 6},
    ]

    created_categories = {}
    for cat_data in categories_data:
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

def create_subcategories(db: Session, categories: dict):
    """Create 36 subcategories (6 per main UI category)"""
    subcategories_by_category = {
        "Forbidden Desires": [
            ("step_sisters", "Naughty step-sisters who love to tease."),
            ("teachers", "Seductive teachers with irresistible lessons."),
            ("roommates", "Playful roommates creating intimate moments."),
            ("bosses", "Powerful bosses with dominant charm."),
            ("neighbors", "Flirty neighbors next door."),
            ("ex_lovers", "Irresistible ex-lovers you can’t forget."),
        ],
        "Dirty Talk Queens": [
            ("phone_sex", "Phone sex operators who know exactly what to say."),
            ("cam_girls", "Webcam performers who love to put on a show."),
            ("sexting", "Sexting specialists who heat up your screen."),
            ("voice_actors", "Erotic voice artists with intoxicating tones."),
            ("chat_hosts", "Chat room hosts who keep the pleasure flowing."),
            ("flirt_coaches", "Flirtation coaches who teach the art of seduction."),
        ],
        "Stress Relief Goddesses": [
            ("therapists", "Sensual therapists for intimate healing."),
            ("masseuses", "Erotic masseuses to melt your stress away."),
            ("yoga_instructors", "Tantric yoga teachers to balance body and desire."),
            ("life_coaches", "Motivational goddesses who lift your spirit."),
            ("meditation_guides", "Mindfulness mistresses to calm your mind."),
            ("wellness_experts", "Holistic healers for total relaxation."),
        ],
        "Your Wildest Dreams": [
            ("vampires", "Seductive vampires of eternal passion."),
            ("angels", "Fallen angels with heavenly desire."),
            ("demons", "Tempting demons from the shadows."),
            ("witches", "Enchanting witches casting love spells."),
            ("goddesses", "Divine goddesses of irresistible charm."),
            ("aliens", "Exotic aliens from beyond the stars."),
        ],
        "Secret Confessions": [
            ("confessors", "Secret keepers for your deepest desires."),
            ("counselors", "Intimate counselors who truly understand."),
            ("best_friends", "Naughty best friends you can trust."),
            ("diary_keepers", "Personal diary holders of your heart."),
            ("soul_mates", "Destined soul mates who get you."),
            ("pen_pals", "Erotic pen pals for intimate letters."),
        ],
        "Playful Temptresses": [
            ("comedians", "Naughty comedians who make pleasure fun."),
            ("dancers", "Exotic dancers with hypnotic moves."),
            ("singers", "Sultry singers with velvet voices."),
            ("gamers", "Gamer girls who love playful competition."),
            ("artists", "Erotic artists who paint with passion."),
            ("party_hosts", "Party goddesses who bring the vibe."),
        ],
    }

    created = {}
    for cat_name, subcats in subcategories_by_category.items():
        parent = categories.get(cat_name)
        if not parent:
            print(f"Parent category missing for subcategories: {cat_name}")
            continue
        for sort_order, (slug, desc) in enumerate(subcats, start=1):
            existing = db.query(Subcategory).filter(Subcategory.name == slug).first()
            if not existing:
                sc = Subcategory(
                    name=slug,
                    description=desc,
                    image_url="/assets/avatar1.png",
                    is_active=True,
                    sort_order=sort_order,
                    category_id=parent.id,
                )
                db.add(sc)
                db.commit()
                db.refresh(sc)
                created[slug] = sc
                print(f"Created subcategory: {slug} under {cat_name}")
            else:
                # Ensure it belongs to the correct parent if changed
                if existing.category_id != parent.id:
                    existing.category_id = parent.id
                    db.add(existing)
                    db.commit()
                created[slug] = existing
                print(f"Subcategory already exists: {slug}")
    return created


def create_characters(db: Session, categories: dict, subcategories: dict):
    """Create 36 characters (6 per UI category) and assign subcategories"""
    character_service = CharacterService(db)

    assignments = [
        # Forbidden Desires
        ("luna", "Forbidden Desires", "step_sisters"),
        ("elena", "Forbidden Desires", "teachers"),
        ("aurora", "Forbidden Desires", "roommates"),
        ("victoria", "Forbidden Desires", "bosses"),
        ("valentina", "Forbidden Desires", "neighbors"),
        ("scarlett", "Forbidden Desires", "ex_lovers"),

        # Dirty Talk Queens
        ("maya", "Dirty Talk Queens", "flirt_coaches"),
        ("chloe", "Dirty Talk Queens", "chat_hosts"),
        ("riley", "Dirty Talk Queens", "phone_sex"),
        ("amber", "Dirty Talk Queens", "sexting"),
        ("sophia", "Dirty Talk Queens", "cam_girls"),
        ("jasmine", "Dirty Talk Queens", "voice_actors"),

        # Stress Relief Goddesses
        ("aria", "Stress Relief Goddesses", "life_coaches"),
        ("sunny", "Stress Relief Goddesses", "wellness_experts"),
        ("joy", "Stress Relief Goddesses", "meditation_guides"),
        ("bliss", "Stress Relief Goddesses", "yoga_instructors"),
        ("spark", "Stress Relief Goddesses", "masseuses"),
        ("hope", "Stress Relief Goddesses", "therapists"),

        # Your Wildest Dreams
        ("isabella", "Your Wildest Dreams", "vampires"),
        ("seraphina", "Your Wildest Dreams", "angels"),
        ("nyx", "Your Wildest Dreams", "demons"),
        ("morgana", "Your Wildest Dreams", "witches"),
        ("goddesses", "Your Wildest Dreams", "goddesses"),  # placeholder, will adjust below if missing persona
        ("celeste", "Your Wildest Dreams", "aliens"),

        # Secret Confessions
        ("zara", "Secret Confessions", "confessors"),
        ("eva", "Secret Confessions", "counselors"),
        ("diana", "Secret Confessions", "best_friends"),
        ("ruby", "Secret Confessions", "diary_keepers"),
        ("phoenix", "Secret Confessions", "soul_mates"),
        ("velvet", "Secret Confessions", "pen_pals"),

        # Playful Temptresses
        ("astro_baba", "Playful Temptresses", "comedians"),
        ("jester", "Playful Temptresses", "party_hosts"),
        ("melody", "Playful Temptresses", "singers"),
        ("pixel", "Playful Temptresses", "gamers"),
        ("nova", "Playful Temptresses", "dancers"),
        ("sage", "Playful Temptresses", "artists"),
    ]

    # Adjust for any placeholder: prefer 'luna_wolf' for goddesses if available
    for idx, (p, cat, sub) in enumerate(assignments):
        if p == "goddesses":
            # Use 'luna_wolf' persona if present; else keep 'morgana' duplicate won't be created twice due to name check.
            p2 = "luna_wolf"
            assignments[idx] = (p2, cat, sub)

    for persona_key, category_name, sub_slug in assignments:
        category = categories.get(category_name)
        subcat = subcategories.get(sub_slug)
        if not category or not subcat:
            print(f"Missing category/subcategory for {persona_key}: {category_name} / {sub_slug}")
            continue

        # Check if character already exists by canonical persona name
        persona = CharacterPersonas.get_persona(persona_key)
        if not persona:
            print(f"Persona not found: {persona_key}")
            continue
        existing = db.query(Character).filter(Character.name == persona["name"]).first()
        if not existing:
            try:
                character = character_service.create_character_from_persona(persona_key, category.id)
                # assign subcategory
                character.subcategory_id = subcat.id
                db.add(character)
                db.commit()
                db.refresh(character)
                print(f"Created character: {character.display_name} in {category_name} / {sub_slug}")
            except ValueError as e:
                print(f"Error creating character {persona_key}: {e}")
        else:
            # Ensure category/subcategory attached
            updated = False
            if not existing.category_id:
                existing.category_id = category.id
                updated = True
            if not existing.subcategory_id:
                existing.subcategory_id = subcat.id
                updated = True
            if updated:
                db.add(existing)
                db.commit()
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
        
        # Create categories (6 groups)
        categories = create_categories(db)

        # Create subcategories (36 total)
        subcategories = create_subcategories(db, categories)

        # Create characters and attach to subcategories (36 total)
        create_characters(db, categories, subcategories)

        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
