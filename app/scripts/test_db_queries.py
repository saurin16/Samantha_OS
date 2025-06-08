"""Test various database queries using the schema."""

import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db_connection

def run_test_queries():
    """Run various test queries to demonstrate database functionality."""
    
    # 1. Basic SELECT query
    print("\n1. 📚 Basic Book Query:")
    print("-" * 80)
    query1 = """
    SELECT title, author, price, genre
    FROM books
    LIMIT 3
    """
    result1 = db_connection.execute_query(query1)
    if "rows" in result1:
        for row in result1["rows"]:
            print(f"Title: {row['title']}")
            print(f"Author: {row['author']}")
            print(f"Price: ${row['price']}")
            print(f"Genre: {row['genre']}")
            print("-" * 40)

    # 2. JOIN query
    print("\n2. 📊 Recent Orders with User and Book Details:")
    print("-" * 80)
    query2 = """
    SELECT 
        u.first_name,
        u.last_name,
        b.title,
        o.quantity,
        o.total_amount,
        o.created_at
    FROM orders o
    JOIN users u ON o.user_id = u.id
    JOIN books b ON o.book_id = b.id
    WHERE o.status = 'completed'
    ORDER BY o.created_at DESC
    LIMIT 3
    """
    result2 = db_connection.execute_query(query2)
    if "rows" in result2:
        for row in result2["rows"]:
            print(f"Customer: {row['first_name']} {row['last_name']}")
            print(f"Book: {row['title']}")
            print(f"Quantity: {row['quantity']}")
            print(f"Total: ${row['total_amount']}")
            print(f"Date: {row['created_at']}")
            print("-" * 40)

    # 3. Aggregation query
    print("\n3. 📈 Sales by Genre:")
    print("-" * 80)
    query3 = """
    SELECT 
        b.genre,
        COUNT(DISTINCT o.id) as order_count,
        SUM(o.quantity) as total_books_sold,
        ROUND(SUM(o.total_amount), 2) as total_revenue
    FROM books b
    JOIN orders o ON b.id = o.book_id
    WHERE o.status = 'completed'
    GROUP BY b.genre
    ORDER BY total_revenue DESC
    """
    result3 = db_connection.execute_query(query3)
    if "rows" in result3:
        for row in result3["rows"]:
            print(f"Genre: {row['genre']}")
            print(f"Orders: {row['order_count']}")
            print(f"Books Sold: {row['total_books_sold']}")
            print(f"Revenue: ${row['total_revenue']}")
            print("-" * 40)

    # 4. Date-based query
    print("\n4. 📅 Recent Active Users:")
    print("-" * 80)
    query4 = """
    SELECT 
        first_name,
        last_name,
        email,
        created_at
    FROM users
    WHERE is_active = 1
    ORDER BY created_at DESC
    LIMIT 3
    """
    result4 = db_connection.execute_query(query4)
    if "rows" in result4:
        for row in result4["rows"]:
            print(f"Name: {row['first_name']} {row['last_name']}")
            print(f"Email: {row['email']}")
            print(f"Joined: {row['created_at']}")
            print("-" * 40)

if __name__ == "__main__":
    run_test_queries() 