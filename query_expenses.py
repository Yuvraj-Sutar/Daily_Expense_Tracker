from database import get_connection

connection = get_connection()

query = """
SELECT SUM(amount) AS total_spending
FROM expenses
"""

result = connection.execute(query).fetchone()

print("Total Spending:", result["total_spending"])

connection.close()