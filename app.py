import csv
import io
from flask import make_response
from flask import Flask, render_template, request, redirect, url_for, flash
from expense_operations import (
    add_expense as create_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense as remove_expense,
    get_monthly_expense_report,
    get_category_expense_report
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

    # 1. Total expenses
    total_expenses = sum(
        float(expense["amount"]) for expense in expenses
    )

    # 2. Current month's expenses
    current_month = datetime.now().strftime("%Y-%m")

    monthly_expenses = [
        expense for expense in expenses
        if str(expense["expense_date"]).startswith(current_month)
    ]

    this_month_expenses = sum(
        float(expense["amount"]) for expense in monthly_expenses
    )

    # 3. Total transactions
    total_transactions = len(expenses)

    # 4. Category-wise spending
    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = float(expense["amount"])

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    # 5. Highest spending category
    if category_totals:
        top_category = max(
            category_totals,
            key=category_totals.get
        )
    else:
        top_category = "N/A"

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expenses=total_expenses,
        this_month_expenses=this_month_expenses,
        total_transactions=total_transactions,
        top_category=top_category
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
# 4. DELETE EXPENSE
# ==============================

@app.route("/delete-expense/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):

    try:
        deleted = remove_expense(expense_id)

        if deleted:
            flash("Expense deleted successfully!", "success")
        else:
            flash("Expense not found.", "error")

    except Exception:
        app.logger.exception("Failed to delete expense")
        flash("Unable to delete expense.", "error")

    return redirect(url_for("home"))


# ==============================
# 5. MONTHLY EXPENSE REPORTS
# ==============================


@app.route("/reports")
def reports():

    monthly_reports = get_monthly_expense_report()
    category_reports = get_category_expense_report()

    total_expenses = sum(
        float(row["total_spending"])
        for row in monthly_reports
    )

    highest_month = (
        max(
            monthly_reports,
            key=lambda row: float(row["total_spending"])
        )
        if monthly_reports else None
    )

    # Prepare monthly chart data
    month_labels = [
        row["month"] for row in monthly_reports
    ]

    monthly_totals = [
        float(row["total_spending"])
        for row in monthly_reports
    ]

    # Prepare category chart data
    category_labels = [
        row["category"] for row in category_reports
    ]

    category_totals = [
        float(row["total_spending"])
        for row in category_reports
    ]

    return render_template(
        "reports.html",
        monthly_reports=monthly_reports,
        category_reports=category_reports,
        total_expenses=total_expenses,
        highest_month=highest_month,
        month_labels=month_labels,
        monthly_totals=monthly_totals,
        category_labels=category_labels,
        category_totals=category_totals
    )


    monthly_reports = get_monthly_expense_report()

    category_reports = get_category_expense_report()

    total_expenses = sum(
        float(row["total_spending"])
        for row in monthly_reports
    )

    highest_month = (
        max(
            monthly_reports,
            key=lambda row: float(row["total_spending"])
        )
        if monthly_reports else None
    )

    return render_template(
        "reports.html",
        monthly_reports=monthly_reports,
        category_reports=category_reports,
        total_expenses=total_expenses,
        highest_month=highest_month
    )

# ==============================
# 5. EXPORT EXPENSES TO CSV
# ==============================

@app.route("/export-expenses")
def export_expenses():

    try:
        # Fetch all expense records
        expenses = get_all_expenses()

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)

        # CSV column headings
        writer.writerow([
            "Expense ID",
            "Title",
            "Amount",
            "Category",
            "Expense Date"
        ])

        # Write expense records
        for expense in expenses:
            writer.writerow([
                expense["id"],
                expense["description"],
                expense["amount"],
                expense["category"],
                expense["expense_date"]
            ])

        # Prepare downloadable response
        response = make_response(output.getvalue())

        response.headers["Content-Disposition"] = (
            "attachment; filename=expenses.csv"
        )
        response.headers["Content-Type"] = (
            "text/csv; charset=utf-8"
        )

        return response

    except Exception:
        app.logger.exception("Failed to export expenses")
        flash("Unable to export expenses. Please try again.", "error")
        return redirect(url_for("home"))


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
