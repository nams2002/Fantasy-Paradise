#!/usr/bin/env python3
"""
Fix boolean values in database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from sqlalchemy import text

def fix_booleans():
    """Fix boolean values"""
    
    print("🔧 Fixing boolean values...")
    
    try:
        with engine.connect() as conn:
            # Update characters to have proper boolean values
            result = conn.execute(text("UPDATE characters SET is_active = true WHERE is_active = 1"))
            conn.commit()
            print(f"✅ Updated {result.rowcount} characters")
            
            # Verify the fix
            result = conn.execute(text("SELECT COUNT(*) FROM characters WHERE is_active = true"))
            count = result.scalar()
            print(f"📊 Characters with is_active = true: {count}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_booleans()
