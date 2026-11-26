
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
from database import get_connection

def delete_expense(expense_id):
    conn = get_connection()

    cursor = conn.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return cursor.rowcount > 0

# 6. MONTHLY EXPENSE REPORT

def get_monthly_expense_report():

    connection = get_connection()

    try:
        query = """
            SELECT
                strftime('%Y-%m', expense_date) AS month,
                COUNT(*) AS total_transactions,
                SUM(amount) AS total_spending
            FROM expenses
            GROUP BY strftime('%Y-%m', expense_date)
            ORDER BY month DESC
        """

        return connection.execute(query).fetchall()

    finally:
        connection.close()


# 7. CATEGORY-WISE EXPENSE REPORT

def get_category_expense_report():

    connection = get_connection()

    try:
        query = """
            SELECT
                category,
                COUNT(*) AS total_transactions,
                SUM(amount) AS total_spending
            FROM expenses
            GROUP BY category
            ORDER BY total_spending DESC
        """

        return connection.execute(query).fetchall()

    finally:
        connection.close()
