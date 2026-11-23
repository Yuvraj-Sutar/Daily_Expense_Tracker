
from flask import Flask, render_template, request, redirect, url_for, flash
from expense_operations import add_expense as create_expense
from expense_operations import get_all_expenses
from datetime import datetime
import math

app = Flask(__name__)
app.secret_key = "daily-expense-tracker-dev-key"

# Allowed expense categories
ALLOWED_CATEGORIES = {
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other"
}


@app.route("/")
def home():

    # Fetch expenses from SQLite
    expenses = get_all_expenses()

    # Calculate total expenses
    total_expenses = sum(
        float(expense["amount"]) for expense in expenses
    )

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expenses=total_expenses
    )


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()

        # Validate expense title
        if not title:
            flash("Expense title cannot be empty.", "error")
            return redirect(url_for("add_expense"))

        if len(title) > 100:
            flash("Expense title cannot exceed 100 characters.", "error")
            return redirect(url_for("add_expense"))

        # Validate amount
        try:
            amount = float(amount_text)

            if not math.isfinite(amount) or amount < 0.01:
                raise ValueError

        except (ValueError, TypeError):
            flash(
                "Please enter a valid amount of at least ₹0.01.",
                "error"
            )
            return redirect(url_for("add_expense"))

        # Validate category
        if category not in ALLOWED_CATEGORIES:
            flash("Please select a valid expense category.", "error")
            return redirect(url_for("add_expense"))

        # Validate date
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")

        except ValueError:
            flash("Please enter a valid expense date.", "error")
            return redirect(url_for("add_expense"))

        # Save expense to SQLite
        try:
            create_expense(
                amount,
                category,
                title,
                expense_date
            )

            flash("Expense added successfully!", "success")
            return redirect(url_for("home"))

        except Exception:
            app.logger.exception("Failed to save expense")
            flash(
                "Unable to save expense. Please try again.",
                "error"
            )
            return redirect(url_for("add_expense"))

    return render_template("add_expense.html")


if __name__ == "__main__":
    app.run(debug=True)
