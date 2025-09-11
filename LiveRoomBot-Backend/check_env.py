#!/usr/bin/env python3
"""
Check environment variables
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def check_env():
    """Check environment variables"""
    
    print("🔍 Checking environment variables...")
    
    print(f"📊 DATABASE_URL from settings: {settings.DATABASE_URL}")
    print(f"📊 DATABASE_URL from os.getenv: {os.getenv('DATABASE_URL')}")
    print(f"📊 Current working directory: {os.getcwd()}")
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env file exists")
        with open(env_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('DATABASE_URL'):
                    print(f"📊 .env DATABASE_URL: {line.strip()}")
    else:
        print(f"❌ .env file not found")
    
    # Check if python-dotenv is being used
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv is available")
        load_dotenv()
        print(f"📊 DATABASE_URL after load_dotenv: {os.getenv('DATABASE_URL')}")
    except ImportError:
        print("❌ python-dotenv not available")

if __name__ == "__main__":
    check_env()
