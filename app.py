
from flask import Flask, render_template, request, redirect, url_for, flash
from expense_operations import (
    add_expense as create_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense
)
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


# ==============================
# 1. HOME / VIEW EXPENSES
# ==============================

@app.route("/")
def home():

    expenses = get_all_expenses()

    total_expenses = sum(
        float(expense["amount"]) for expense in expenses
    )

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expenses=total_expenses
    )


# ==============================
# 2. ADD EXPENSE
# ==============================

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()

        # Validate title
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
                "Please enter a valid amount of at least 0.01.",
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

        # Save to SQLite
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


# ==============================
# 3. EDIT / UPDATE EXPENSE
# ==============================

@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):

    # Get existing expense
    expense = get_expense_by_id(expense_id)

    if expense is None:
        flash("Expense not found.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()

        # Validate title
        if not title or len(title) > 100:
            flash("Please enter a valid expense title.", "error")
            return redirect(url_for(
                "edit_expense",
                expense_id=expense_id
            ))

        # Validate amount
        try:
            amount = float(amount_text)

            if not math.isfinite(amount) or amount < 0.01:
                raise ValueError

        except (ValueError, TypeError):
            flash(
                "Please enter a valid amount of at least 0.01.",
                "error"
            )
            return redirect(url_for(
                "edit_expense",
                expense_id=expense_id
            ))

        # Validate category
        if category not in ALLOWED_CATEGORIES:
            flash("Please select a valid category.", "error")
            return redirect(url_for(
                "edit_expense",
                expense_id=expense_id
            ))

        # Validate date
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")

        except ValueError:
            flash("Please enter a valid date.", "error")
            return redirect(url_for(
                "edit_expense",
                expense_id=expense_id
            ))

        # Update SQLite record
        try:
            updated = update_expense(
                expense_id,
                amount,
                category,
                title,
                expense_date
            )

            if updated:
                flash("Expense updated successfully!", "success")
            else:
                flash("No expense was updated.", "error")

            return redirect(url_for("home"))

        except Exception:
            app.logger.exception("Failed to update expense")
            flash("Unable to update expense.", "error")
            return redirect(url_for(
                "edit_expense",
                expense_id=expense_id
            ))

    return render_template(
        "edit_expense.html",
        expense=expense
    )


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
