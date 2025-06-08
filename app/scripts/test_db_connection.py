"""Test database connection and run a sample query."""

import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db_connection

def test_connection():
    """Test database connection and run a sample query."""
    # Test a simple query
    query = """
    SELECT b.title, b.author, b.price, b.genre
    FROM books b
    LIMIT 5
    """
    
    result = db_connection.execute_query(query)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    if "rows" in result:
        print("\n📚 Sample Books from Database:")
        print("-" * 80)
        for row in result["rows"]:
            print(f"Title: {row['title']}")
            print(f"Author: {row['author']}")
            print(f"Price: ${row['price']}")
            print(f"Genre: {row['genre']}")
            print("-" * 80)
    else:
        print("No results found")

if __name__ == "__main__":
    test_connection() 