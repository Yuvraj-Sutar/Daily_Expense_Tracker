
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage (we will replace this with MySQL)
expenses = []


@app.route("/")
def home():
    total_expenses = sum(expense["amount"] for expense in expenses)

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expenses=total_expenses
    )


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount = request.form.get("amount", type=float)
        category = request.form.get("category")
        date = request.form.get("date")

        if not title or amount is None or amount <= 0 or not category or not date:
            return "Please enter valid expense details.", 400

        expense = {
            "title": title,
            "amount": amount,
            "category": category,
            "date": date
        }

        expenses.append(expense)

        return redirect(url_for("home"))

    return render_template("add_expense.html")


if __name__ == "__main__":
    app.run(debug=True)
