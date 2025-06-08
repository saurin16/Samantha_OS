"""Simple SQLite database connection test."""

import sqlite3
import os

def test_simple_connection():
    """Test direct SQLite connection."""
    # Database path
    db_path = r"C:\Users\patel\Desktop\GENAI_NLP\Agentic-AI\samantha_os\samantha-os1-main\scratchpad\bookstore.db"
    
    print("\n🔍 Database Path:")
    print("-" * 80)
    print(f"Path: {db_path}")
    print(f"Exists: {os.path.exists(db_path)}")
    
    try:
        # Try to connect
        print("\n🔌 Testing Connection:")
        print("-" * 80)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test a simple query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n📚 Available Tables:")
        print("-" * 80)
        for table in tables:
            print(f"- {table[0]}")
            
            # Show table structure
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  • {col[1]} ({col[2]})")
            print()
        
        conn.close()
        print("✅ Connection test successful!")
        
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")

if __name__ == "__main__":
    test_simple_connection() 