
from database import get_connection

connection = get_connection()

query = """
SELECT name
FROM sqlite_master
WHERE type = 'table'
"""

tables = connection.execute(query).fetchall()

print("Database tables:")

for table in tables:
    print("-", table["name"])

connection.close()
