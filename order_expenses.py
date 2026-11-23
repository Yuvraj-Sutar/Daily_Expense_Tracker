
from database import get_connection

connection = get_connection()

# Sort expenses by amount (highest first)
query = """
SELECT * FROM expenses
ORDER BY amount ASC
"""

expenses = connection.execute(query).fetchall()

print("\n----- EXPENSES: HIGH TO LOW -----")

for expense in expenses:
    print("ID:", expense["id"])
    print("Category:", expense["category"])
    print("Description:", expense["description"])
    print("Amount:", expense["amount"])
    print("------------------------")

connection.close()
