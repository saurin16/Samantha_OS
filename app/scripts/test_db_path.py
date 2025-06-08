"""Test database path and connection."""

import os
import sys
from sqlalchemy import text

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db_connection, db_config

def test_db_path():
    """Test database path and connection."""
    print("\n🔍 Database Configuration:")
    print("-" * 80)
    print(f"Dialect: {db_config.dialect}")
    print(f"Database: {db_config.database}")
    
    # Use the same path as in the connection string
    db_path = r"C:\Users\patel\Desktop\GENAI_NLP\Agentic-AI\samantha_os\samantha-os1-main\scratchpad\bookstore.db"
    print(f"\n📂 Database Path:")
    print(f"Absolute: {db_path}")
    print(f"Exists: {os.path.exists(db_path)}")
    
    # Test connection
    print("\n🔌 Testing Connection:")
    print("-" * 80)
    if db_connection._engine:
        print("✅ Database engine created")
        try:
            with db_connection._engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Connection test successful")
        except Exception as e:
            print(f"❌ Connection test failed: {str(e)}")
    else:
        print("❌ Database engine not created")

if __name__ == "__main__":
    test_db_path() 