
from database import get_connection


def add_expense(amount, category, description, expense_date):

    connection = get_connection()

    query = """
    INSERT INTO expenses
    (amount, category, description, expense_date)
    VALUES (?, ?, ?, ?)
    """

    connection.execute(
        query,
        (amount, category, description, expense_date)
    )

    connection.commit()
    connection.close()

    print("Expense added successfully!")


# Test the function
add_expense(
    350,
    "Entertainment",
    "Movie ticket",
    "2026-11-23"
)
