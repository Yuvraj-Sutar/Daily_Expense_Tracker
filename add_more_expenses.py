
from database import get_connection

connection = get_connection()

expenses = [
    (250, "Shopping", "Notebook", "2026-11-22"),
    (80, "Travel", "Bus ticket", "2026-11-22")
]

query = """
INSERT INTO expenses
(amount, category, description, expense_date)
VALUES (?, ?, ?, ?)
"""

connection.executemany(query, expenses)
connection.commit()

print("Two expenses added successfully!")

connection.close()
