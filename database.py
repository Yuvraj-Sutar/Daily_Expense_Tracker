
import sqlite3
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Database directory
DB_DIR = BASE_DIR / "database"

# Create database folder if it doesn't exist
DB_DIR.mkdir(exist_ok=True)

# Database file location
DB_PATH = DB_DIR / "expense_tracker.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():

    connection = get_connection()

    schema_path = BASE_DIR / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    connection.executescript(sql_script)

    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


if __name__ == "__main__":
    init_db()
