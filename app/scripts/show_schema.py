"""Script to display the complete database schema."""

import sqlite3
from pathlib import Path
from utils.common import logger

def show_database_schema():
    """Display the complete database schema."""
    try:
        # Get the absolute path to the database file
        db_path = Path(r"C:\Users\patel\Desktop\GENAI_NLP\Agentic-AI\samantha_os\samantha-os1-main\scratchpad\bookstore.db")
        
        if not db_path.exists():
            logger.error(f"❌ Database file not found at: {db_path}")
            return

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        logger.info("📚 Database Schema:")
        logger.info("=" * 50)

        for table in tables:
            table_name = table[0]
            logger.info(f"\n📋 Table: {table_name}")
            logger.info("-" * 30)

            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            # Print column information
            for col in columns:
                col_id, name, type_, notnull, default_value, pk = col
                constraints = []
                if pk:
                    constraints.append("PRIMARY KEY")
                if notnull:
                    constraints.append("NOT NULL")
                if default_value is not None:
                    constraints.append(f"DEFAULT {default_value}")
                
                constraint_str = " ".join(constraints)
                logger.info(f"  • {name} ({type_}) {constraint_str}")

            # Get sample data (first row)
            try:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
                sample = cursor.fetchone()
                if sample:
                    logger.info("\n  Sample Data:")
                    for col, val in zip(columns, sample):
                        logger.info(f"    {col[1]}: {val}")
            except sqlite3.Error as e:
                logger.warning(f"  Could not fetch sample data: {str(e)}")

        conn.close()
        logger.info("\n✅ Schema display completed successfully")

    except Exception as e:
        logger.error(f"❌ Error displaying schema: {str(e)}")

if __name__ == "__main__":
    show_database_schema() 