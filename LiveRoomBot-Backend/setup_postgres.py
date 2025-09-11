#!/usr/bin/env python3
"""
Script to set up PostgreSQL database for LiveRoom
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass
import sys

def setup_database():
    """Set up the PostgreSQL database and user for LiveRoom"""
    
    # Get PostgreSQL admin credentials
    print("Setting up PostgreSQL database for LiveRoom...")
    print("Please enter your PostgreSQL admin credentials:")
    
    admin_user = input("PostgreSQL admin username (default: postgres): ").strip() or "postgres"
    admin_password = getpass.getpass("PostgreSQL admin password: ")
    host = input("PostgreSQL host (default: localhost): ").strip() or "localhost"
    port = input("PostgreSQL port (default: 5432): ").strip() or "5432"
    
    try:
        # Connect to PostgreSQL as admin
        print(f"\nConnecting to PostgreSQL at {host}:{port}...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            database="postgres"  # Connect to default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create database
        print("Creating database 'liveroom_db'...")
        try:
            cursor.execute("CREATE DATABASE liveroom_db;")
            print("✓ Database 'liveroom_db' created successfully!")
        except psycopg2.errors.DuplicateDatabase:
            print("✓ Database 'liveroom_db' already exists!")
        
        # Create user
        print("Creating user 'liveroom_user'...")
        try:
            cursor.execute("CREATE USER liveroom_user WITH PASSWORD 'liveroom_password';")
            print("✓ User 'liveroom_user' created successfully!")
        except psycopg2.errors.DuplicateObject:
            print("✓ User 'liveroom_user' already exists!")
            # Update password just in case
            cursor.execute("ALTER USER liveroom_user WITH PASSWORD 'liveroom_password';")
            print("✓ Password updated for 'liveroom_user'!")
        
        # Grant privileges
        print("Granting privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE liveroom_db TO liveroom_user;")
        cursor.execute("ALTER USER liveroom_user CREATEDB;")  # Allow creating test databases
        print("✓ Privileges granted successfully!")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostgreSQL setup completed successfully!")
        print("\nDatabase connection details:")
        print(f"  Host: {host}")
        print(f"  Port: {port}")
        print(f"  Database: liveroom_db")
        print(f"  Username: liveroom_user")
        print(f"  Password: liveroom_password")
        print(f"\nConnection URL: postgresql://liveroom_user:liveroom_password@{host}:{port}/liveroom_db")
        
        # Test connection with new user
        print("\nTesting connection with new user...")
        test_conn = psycopg2.connect(
            host=host,
            port=port,
            user="liveroom_user",
            password="liveroom_password",
            database="liveroom_db"
        )
        test_conn.close()
        print("✓ Connection test successful!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ PostgreSQL Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    if setup_database():
        print("\n✅ You can now run the database migrations!")
        print("Run: alembic upgrade head")
    else:
        print("\n❌ Setup failed. Please check your PostgreSQL installation and credentials.")
        sys.exit(1)
