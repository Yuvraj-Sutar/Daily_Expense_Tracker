
from database import get_connection

connection = get_connection()

query = """
SELECT category, SUM(amount) AS total
FROM expenses
GROUP BY category
"""

results = connection.execute(query).fetchall()

print("\n----- CATEGORY WISE SPENDING -----")

for expense in results:
    print(
        expense["category"],
        ":", expense["total"]
    )

connection.close()
