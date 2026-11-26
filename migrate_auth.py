import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "database" / "expense_tracker.db"

def migrate_database():
    conn = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("PRAGMA table_info(expenses)")
        columns = [column[1] for column in cursor.fetchall()]

        if "user_id" not in columns:
            cursor.execute("""
                ALTER TABLE expenses
                ADD COLUMN user_id INTEGER REFERENCES users(id)
            """)
            print("user_id column added successfully.")
        else:
            print("user_id column already exists.")

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expenses_user_id
            ON expenses(user_id)
        """)

        conn.commit()

        print("Database migration successful!")
        print("Users table ready.")

        print("Total existing expenses:",
              cursor.execute("SELECT COUNT(*) FROM expenses").fetchone()[0])

        print("Total registered users:",
              cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0])

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    migrate_database()
