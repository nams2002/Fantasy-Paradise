#!/usr/bin/env python3
"""
Check PostgreSQL database directly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import psycopg2
from app.core.config import settings

def check_postgres():
    """Check PostgreSQL database directly"""
    
    print("🔍 Checking PostgreSQL database directly...")
    
    try:
        # Parse DATABASE_URL
        db_url = settings.DATABASE_URL
        print(f"📊 Database URL: {db_url}")
        
        # Connect directly to PostgreSQL
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Check characters table
        cursor.execute("SELECT COUNT(*) FROM characters")
        total_count = cursor.fetchone()[0]
        print(f"📊 Total characters in PostgreSQL: {total_count}")
        
        # Check active characters
        cursor.execute("SELECT COUNT(*) FROM characters WHERE is_active = true")
        active_true_count = cursor.fetchone()[0]
        print(f"📊 Active characters (is_active = true): {active_true_count}")
        
        cursor.execute("SELECT COUNT(*) FROM characters WHERE is_active = 1")
        active_one_count = cursor.fetchone()[0]
        print(f"📊 Active characters (is_active = 1): {active_one_count}")
        
        # Show some sample characters
        cursor.execute("SELECT id, name, display_name, is_active FROM characters LIMIT 10")
        characters = cursor.fetchall()
        print(f"\n📋 Sample characters:")
        for char in characters:
            print(f"  ID: {char[0]}, Name: {char[1]}, Display: {char[2]}, Active: {char[3]} (type: {type(char[3])})")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_postgres()
