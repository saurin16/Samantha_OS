"""Database configuration and connection management."""

import os
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from utils.common import logger


class DatabaseConfig(BaseModel):
    """Database configuration."""

    dialect: str = Field(..., description="Database dialect (e.g., 'sqlite', 'postgresql')")
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    database: str = Field(..., description="Database name or file path (for SQLite)")


class DatabaseConnection:
    """Manages database connections and operations."""

    def __init__(self):
        self._engine = None
        self._connection_string = None

    def connect(self, config: DatabaseConfig) -> bool:
        """Creates a database connection based on the provided configuration."""
        try:
            # Hardcoded SQLite configuration
            db_path = r"C:\Users\patel\Desktop\GENAI_NLP\Agentic-AI\samantha_os\samantha-os1-main\scratchpad\bookstore.db"
            if not os.path.exists(db_path):
                raise FileNotFoundError(f"Database file not found at: {db_path}")
            
            # Use three forward slashes for absolute path in SQLite URL
            self._connection_string = f"sqlite:///{db_path}"
            self._engine = create_engine(self._connection_string)

            # Test the connection
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info(f"✅ Connected to SQLite database at: {db_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Error connecting to DB: {str(e)}")
            return False

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Executes a SQL query and returns results or errors."""
        if not self._engine:
            return {"error": "No database connection established"}

        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(query))

                if query.strip().lower().startswith("select"):
                    columns = result.keys()
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    return {"columns": columns, "rows": rows}
                else:
                    return {"affected_rows": result.rowcount}

        except Exception as e:
            logger.error(f"❌ Query execution error: {str(e)}")
            return {"error": str(e)}


# Create database connection with hardcoded values
db_config = DatabaseConfig(
    dialect="sqlite",
    database=r"C:\Users\patel\Desktop\GENAI_NLP\Agentic-AI\samantha_os\samantha-os1-main\scratchpad\bookstore.db"
)

# Create the database connection instance
db_connection = DatabaseConnection()
db_connection.connect(db_config)

# Dialect-specific prompt support (used in AI generation)
dialect_info = {
    "sqlite": {
        "notes": """
        - Use SQLite date/time functions (strftime, datetime)
        - Use 'date("now")' for current date
        - Dates are stored as TEXT in ISO format
        - Available tables:
          * users (id, first_name, last_name, email, created_at, is_active)
          * books (id, title, author, status, created_at)
        """,
        "examples": """
        - Last month's data:
            WHERE created_at >= date('now', 'start of month', '-1 month')
            AND created_at < date('now', 'start of month')
        """
    }
}
