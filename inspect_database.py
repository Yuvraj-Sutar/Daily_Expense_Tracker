
import sqlite3

DB_PATH = "database/expense_tracker.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

print("\n========== DATABASE TABLES ==========")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()
print(tables)

print("\n========== EXPENSE TABLE COLUMNS ==========")

cursor.execute("PRAGMA table_info(expenses)")

columns = cursor.fetchall()

for column in columns:
    print(column)

print("\n========== EXISTING EXPENSE COUNT ==========")

cursor.execute("SELECT COUNT(*) FROM expenses")

count = cursor.fetchone()[0]

print("Total expenses:", count)

connection.close()

print("\n========== USERS TABLE ==========")

cursor.execute("SELECT COUNT(*) FROM users")
print("Total users:", cursor.fetchone()[0])

print("\n========== EXPENSE OWNERSHIP ==========")

cursor.execute("""
    SELECT
        COUNT(*) AS total,
        COUNT(user_id) AS assigned,
        COUNT(*) - COUNT(user_id) AS unassigned
    FROM expenses
""")

print(dict(cursor.fetchone()))