
from database import get_connection


# 1. CREATE - Add a new expense
def add_expense(amount, category, description, expense_date):

    connection = get_connection()

    try:
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
        return True

    finally:
        connection.close()


# 2. READ - Get all expenses
def get_all_expenses():

    connection = get_connection()

    try:
        query = "SELECT * FROM expenses ORDER BY id DESC"

        expenses = connection.execute(query).fetchall()

        return expenses

    finally:
        connection.close()


# 3. READ - Get one expense using ID
def get_expense_by_id(expense_id):

    connection = get_connection()

    try:
        query = "SELECT * FROM expenses WHERE id = ?"

        expense = connection.execute(
            query, (expense_id,)
        ).fetchone()

        return expense

    finally:
        connection.close()


# 4. UPDATE - Edit an existing expense
def update_expense(
    expense_id, amount, category, description, expense_date
):

    connection = get_connection()

    try:
        query = """
        UPDATE expenses
        SET amount = ?,
            category = ?,
            description = ?,
            expense_date = ?
        WHERE id = ?
        """

        cursor = connection.execute(
            query,
            (amount, category, description, expense_date, expense_id)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# 5. DELETE - Remove an expense
def delete_expense(expense_id):

    connection = get_connection()

    try:
        query = "DELETE FROM expenses WHERE id = ?"

        cursor = connection.execute(
            query, (expense_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()
