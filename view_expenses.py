
from database import get_connection

connection = get_connection()

query = """
SELECT * FROM expenses
"""

expenses = connection.execute(query).fetchall()

print("\n----- ALL EXPENSES -----")

for expense in expenses:
    print("ID:", expense["id"])
    print("Amount:", expense["amount"])
    print("Category:", expense["category"])
    print("Description:", expense["description"])
    print("Date:", expense["expense_date"])
    print("------------------------")

connection.close()
