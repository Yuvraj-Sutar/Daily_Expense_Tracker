
from database import get_connection

connection = get_connection()

# SQL WHERE query
query = """
SELECT * FROM expenses
WHERE category = ?
"""

category =  "Travel"

expenses = connection.execute(
    query, (category,)
).fetchall()

print("\n----- TRAVEL EXPENSES -----")

for expense in expenses:
    print("ID:", expense["id"])
    print("Category:", expense["category"])
    print("Description:", expense["description"])
    print("Amount:", expense["amount"])

connection.close()
