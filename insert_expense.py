
from database import get_connection

# Connect to database
connection = get_connection()

# Expense details
amount = 150
category = "Food"
description = "Lunch"
expense_date = "2026-11-22"

# SQL INSERT query
query = """
INSERT INTO expenses
(amount, category, description, expense_date)
VALUES (?, ?, ?, ?)
"""

# Execute query
connection.execute(
    query,
    (amount, category, description, expense_date)
)

# Save changes
connection.commit()

print("Expense added successfully!")

# Close connection
connection.close()
