

from expense_operations import add_expense, delete_expense

# Restore the original Entertainment expense
add_expense(
    350,
    "Entertainment",
    "Movie ticket",
    "2026-11-23"
)

print("Original expense restored!")

# Remove the temporary test expense
deleted = delete_expense(5)

print("Temporary test expense deleted:", deleted)
