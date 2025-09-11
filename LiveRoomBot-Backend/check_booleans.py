#!/usr/bin/env python3
"""
Check boolean values in database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from sqlalchemy import text

def check_booleans():
    """Check boolean values"""
    
    print("🔍 Checking boolean values...")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, is_active FROM characters"))
            chars = result.fetchall()
            
            print("📊 Characters:")
            for c in chars:
                print(f"  ID: {c[0]}, Name: {c[1]}, Active: {c[2]} (type: {type(c[2])})")
                
            # Test different boolean queries
            print("\n🧪 Testing boolean queries:")
            
            # Test with True
            result = conn.execute(text("SELECT COUNT(*) FROM characters WHERE is_active = true"))
            count_true = result.scalar()
            print(f"  is_active = true: {count_true}")
            
            # Test with 1
            result = conn.execute(text("SELECT COUNT(*) FROM characters WHERE is_active = 1"))
            count_one = result.scalar()
            print(f"  is_active = 1: {count_one}")
            
            # Test with Python True
            result = conn.execute(text("SELECT COUNT(*) FROM characters WHERE is_active = :active"), {"active": True})
            count_py_true = result.scalar()
            print(f"  is_active = Python True: {count_py_true}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_booleans()
