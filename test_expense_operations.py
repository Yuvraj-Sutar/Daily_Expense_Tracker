
from expense_operations import (
    add_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense
)

# CREATE
print("\n1. TESTING CREATE")

add_expense(
    350,
    "Testing",
    "Temporary test expense",
    "2026-11-23"
)

print("Expense added successfully!")


# READ
print("\n2. TESTING READ")

expenses = get_all_expenses()

for expense in expenses:
    print(
        expense["id"],
        expense["category"],
        expense["description"],
        expense["amount"]
    )


# GET ONE RECORD
print("\n3. TESTING SINGLE EXPENSE")

expense = get_expense_by_id(4)

if expense:
    print(dict(expense))
else:
    print("Expense not found")


# UPDATE
print("\n4. TESTING UPDATE")

updated = update_expense(
    4,
    400,
    "Testing",
    "Updated test expense",
    "2026-11-23"
)

print("Updated:", updated)


# DELETE
print("\n5. TESTING DELETE")

deleted = delete_expense(4)

print("Deleted:", deleted)


# VERIFY DELETE
print("\n6. VERIFY DELETE")

expense = get_expense_by_id(4)

if expense is None:
    print("Test expense successfully deleted!")
else:
    print("Test expense still exists!")
