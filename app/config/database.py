"""Database configuration and connection management."""

import os
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from utils.common import logger


class DatabaseConfig(BaseModel):
    """Database configuration."""

    dialect: str = Field(
        ...,
        description="Database dialect (e.g., 'postgresql', 'mysql', 'sqlite')",
    )
    username: Optional[str] = Field(
        None,
        description="Database username",
    )
    password: Optional[str] = Field(
        None,
        description="Database password",
    )
    host: Optional[str] = Field(
        None,
        description="Database host",
    )
    port: Optional[int] = Field(
        None,
        description="Database port",
    )
    database: str = Field(
        ...,
        description="Database name",
    )


class DatabaseConnection:
    """Manages database connections and operations."""

    def __init__(self):
        self._engine = None
        self._connection_string = None

    def connect(self, config: DatabaseConfig) -> bool:
        """Creates a database connection based on the provided configuration."""
        try:
            # Build connection string based on dialect
            if config.dialect == "sqlite":
                self._connection_string = f"sqlite:///{config.database}"
            else:
                # For PostgreSQL, MySQL, etc.
                auth = f"{config.username}:{config.password}@" if config.username else ""
                host = f"{config.host}:{config.port}" if config.host else "localhost"
                self._connection_string = f"{config.dialect}://{auth}{host}/{config.database}"

            self._engine = create_engine(self._connection_string)
            # Test connection
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info(f"Successfully connected to {config.dialect} database: {config.database}")
            return True

        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            return False

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Executes a SQL query and returns the results."""
        if not self._engine:
            return {"error": "No database connection established"}

        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(query))

                if query.strip().lower().startswith("select"):
                    # For SELECT queries, return the results
                    columns = result.keys()
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    return {"columns": columns, "rows": rows}
                else:
                    # For INSERT, UPDATE, DELETE queries, return affected rows
                    return {"affected_rows": result.rowcount}

        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return {"error": str(e)}


# Create a global database connection instance
db_connection = DatabaseConnection()

# Configure the database connection from environment variables or configuration file
db_config = DatabaseConfig(
    dialect=os.getenv("DB_DIALECT", "sqlite"),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432) if os.getenv("DB_PORT") else None,
    database=os.getenv("DB_DATABASE", "database.db"),
)

# Initialize the database connection
db_connection.connect(db_config)

# Get database dialect-specific information
dialect_info = {
    "sqlite": {
        "notes": """
        - Use SQLite date/time functions (strftime, datetime)
        - For current date, use 'date("now")'
        - For date arithmetic, use strftime functions
        - Dates are stored as TEXT in ISO format (YYYY-MM-DD HH:MM:SS)
        """,
        "examples": """
        - Last month's data: 
            WHERE created_at >= date('now', 'start of month', '-1 month') 
            AND created_at < date('now', 'start of month')
        """,
    },
    "postgresql": {
        "notes": """
        - Use PostgreSQL date/time functions (date_trunc, interval)
        - For current date, use CURRENT_DATE
        - For date arithmetic, use interval
        - Dates are stored in native timestamp format
        """,
        "examples": """
        - Last month's data:
            WHERE created_at >= date_trunc('month', current_date - interval '1 month')
            AND created_at < date_trunc('month', current_date)
        """,
    },
}
