"""Expense, attendance, grading, and billing manager (Python 3.8+)."""

from datetime import date


EXPENSE_CATEGORIES = ("Food", "Travel", "Utilities", "Stationery", "Other")
SUBJECTS = ("Maths", "Science", "English", "Computer", "History")
DEFAULT_TAX_RATE = 0.18


def money(value):
    """Return a number in the consistent two-decimal money format."""
    return f"{value:.2f}"


def get_int(prompt, minimum=None, maximum=None):
    """Ask until an integer inside the requested range is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Enter a number of at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a number no greater than {maximum}.")
            continue
        return value


def get_float(prompt, minimum=None, maximum=None):
    """Ask until a numeric value inside the requested range is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Enter a number of at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a number no greater than {maximum}.")
            continue
        return value


def get_name(prompt, minimum=2, maximum=40):
    """Read a non-empty name containing only letters, spaces, or hyphens."""
    while True:
        value = input(prompt).strip()
        if minimum <= len(value) <= maximum and all(
            char.isalpha() or char.isspace() or char == "-" for char in value
        ):
            return " ".join(value.split())
        print(f"Use {minimum}-{maximum} letters, spaces, or hyphens for the name.")


def grade_for(average):
    """Map a percentage to the grading scale in the requirements."""
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    if average >= 35:
        return "E"
    return "F"


def attendance_status(percentage):
    """Return the specified attendance eligibility label."""
    if percentage >= 75:
        return "Eligible"
    if percentage >= 60:
        return "Warning"
    return "Shortage"


def discount_rate(subtotal):
    """Return the bill discount rate for the subtotal slabs."""
    if subtotal >= 10000:
        return 0.15
    if subtotal >= 5000:
        return 0.10
    if subtotal >= 1000:
        return 0.05
    return 0.0


def calculate_invoice(items, tax_rate=DEFAULT_TAX_RATE):
    """Calculate line totals, slab discount, tax after discount, and final total."""
    prepared_items = []
    subtotal = 0.0
    for item in items:
        line_total = round(item["unit_price"] * item["quantity"], 2)
        prepared_items.append({**item, "line_total": line_total})
        subtotal += line_total
    subtotal = round(subtotal, 2)
    rate = discount_rate(subtotal)
    discount = round(subtotal * rate, 2)
    taxable = round(subtotal - discount, 2)
    tax = round(taxable * tax_rate, 2)
    return {
        "items": prepared_items,
        "subtotal": subtotal,
        "discount_rate": rate,
        "discount": discount,
        "taxable": taxable,
        "tax": tax,
        "tax_rate": tax_rate,
        "total": round(taxable + tax, 2),
    }


def expense_summary(expenses):
    """Summarize expenses by category and identify highest/lowest entries."""
    totals = {category: 0.0 for category in EXPENSE_CATEGORIES}
    for expense in expenses:
        totals[expense["category"]] += expense["amount"]
    highest = max(expenses, key=lambda row: row["amount"], default=None)
    lowest = min(expenses, key=lambda row: row["amount"], default=None)
    return {
        "category_totals": {key: round(value, 2) for key, value in totals.items()},
        "grand_total": round(sum(totals.values()), 2),
        "highest": highest,
        "lowest": lowest,
    }


def attendance_summary(records, total_days):
    """Build individual and class attendance totals."""
    rows = []
    for record in records:
        percentage = (record["present"] / total_days * 100) if total_days else 0.0
        rows.append({**record, "percentage": percentage,
                     "status": attendance_status(percentage)})
    percentages = [row["percentage"] for row in rows]
    return {
        "records": rows,
        "total_days": total_days,
        "total_people": len(rows),
        "average": sum(percentages) / len(percentages) if percentages else 0.0,
        "highest": max(rows, key=lambda row: row["percentage"], default=None),
        "lowest": min(rows, key=lambda row: row["percentage"], default=None),
        "counts": {label: sum(row["status"] == label for row in rows)
                   for label in ("Eligible", "Warning", "Shortage")},
    }


def grade_student(student):
    """Calculate a student's total, average, grade, and pass/fail result."""
    marks = list(student["marks"].values())
    total = sum(marks)
    average = total / len(marks) if marks else 0.0
    failed_subject = any(mark < 35 for mark in marks)
    return {**student, "total": total, "average": average,
            "grade": grade_for(average), "result": "FAIL" if failed_subject else "PASS"}


def grade_summary(students):
    """Return class-level averages and pass/fail counts."""
    rows = [grade_student(student) for student in students]
    return {
        "students": rows,
        "class_average": (sum(row["average"] for row in rows) / len(rows)
                          if rows else 0.0),
        "pass_count": sum(row["result"] == "PASS" for row in rows),
        "fail_count": sum(row["result"] == "FAIL" for row in rows),
    }


def format_expense_report(expenses):
    summary = expense_summary(expenses)
    lines = ["EXPENSE REPORT", "Description                 Category      Amount",
             "-" * 52]
    if not expenses:
        lines.append("No expense records available.")
    else:
        for row in expenses:
            lines.append(f"{row['description'][:27]:27} {row['category']:<12} {money(row['amount']):>8}")
    lines.extend(["-" * 52, f"{'Category totals:':27}"])
    for category, amount in summary["category_totals"].items():
        lines.append(f"  {category:<24} {money(amount):>8}")
    lines.append(f"Grand total: {money(summary['grand_total'])}")
    if summary["highest"]:
        lines.append(f"Highest expense: {summary['highest']['description']} ({money(summary['highest']['amount'])})")
        lines.append(f"Lowest expense: {summary['lowest']['description']} ({money(summary['lowest']['amount'])})")
    return "\n".join(lines)


def format_attendance_report(records, total_days):
    summary = attendance_summary(records, total_days)
    lines = ["ATTENDANCE REPORT", f"Working days: {total_days}",
             "Name                 ID       Present   Attendance   Status",
             "-" * 68]
    if not summary["records"]:
        lines.append("No attendance records available.")
    for row in summary["records"]:
        lines.append(f"{row['name'][:20]:20} {row['id'][:8]:8} {row['present']:>7}"
                     f" {row['percentage']:>10.2f}%   {row['status']}")
    lines.append(f"Average attendance: {summary['average']:.2f}%")
    lines.append("Status counts: " + ", ".join(
        f"{key} {value}" for key, value in summary["counts"].items()))
    if summary["highest"]:
        lines.append(f"Highest: {summary['highest']['name']} ({summary['highest']['percentage']:.2f}%)")
        lines.append(f"Lowest: {summary['lowest']['name']} ({summary['lowest']['percentage']:.2f}%)")
    return "\n".join(lines)


def format_grading_report(students):
    summary = grade_summary(students)
    lines = ["GRADING REPORT", "Student              Total    Average   Grade   Result",
             "-" * 58]
    if not summary["students"]:
        lines.append("No student records available.")
    for row in summary["students"]:
        lines.append(f"{row['name'][:20]:20} {row['total']:>5}"
                     f" {row['average']:>10.2f}   {row['grade']:<5}   {row['result']}")
        lines.append("  " + " | ".join(f"{subject}: {mark:g}" for subject, mark in row["marks"].items()))
    lines.append(f"Class average: {summary['class_average']:.2f}%")
    lines.append(f"Pass: {summary['pass_count']} | Fail: {summary['fail_count']}")
    return "\n".join(lines)


def format_invoice(customer, bill_number, invoice):
    """Format a readable invoice with aligned columns and two-decimal values."""
    lines = ["INVOICE", f"Bill No: {bill_number}    Date: {date.today().isoformat()}",
             f"Customer: {customer}", "", "Item                  Unit Price   Qty     Line Total",
             "-" * 58]
    for item in invoice["items"]:
        lines.append(f"{item['name'][:20]:20} {money(item['unit_price']):>10}"
                     f" {item['quantity']:>5} {money(item['line_total']):>14}")
    lines.extend(["-" * 58, f"Subtotal: {money(invoice['subtotal'])}",
                  f"Discount ({invoice['discount_rate']:.0%}): -{money(invoice['discount'])}",
                  f"Taxable amount: {money(invoice['taxable'])}",
                  f"Tax ({invoice['tax_rate']:.0%}): {money(invoice['tax'])}",
                  f"GRAND TOTAL: {money(invoice['total'])}", "Thank you for your purchase!"])
    return "\n".join(lines)


def add_expense(expenses):
    print("\nCategories: " + ", ".join(EXPENSE_CATEGORIES))
    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()
    category = input("Category: ").strip().title()
    while category not in EXPENSE_CATEGORIES:
        print("Choose a category from the list.")
        category = input("Category: ").strip().title()
    amount = get_float("Amount: ", minimum=0.01)
    expenses.append({"description": description, "category": category,
                     "amount": round(amount, 2)})
    print("Expense added successfully.")


def expense_menu(expenses):
    while True:
        print("\nEXPENSE MANAGEMENT\n1. Add expense\n2. View summary\n3. Back")
        choice = get_int("Enter choice (1-3): ", 1, 3)
        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            print(format_expense_report(expenses))
        else:
            return


def attendance_menu(records, state):
    while True:
        print("\nATTENDANCE MANAGEMENT\n1. Set working days\n2. Add attendance record\n3. View summary\n4. Back")
        choice = get_int("Enter choice (1-4): ", 1, 4)
        if choice == 1:
            state["total_days"] = get_int("Total working days: ", 1)
            for row in records:
                row["present"] = min(row["present"], state["total_days"])
            print("Working days updated.")
        elif choice == 2:
            if not state["total_days"]:
                print("Set total working days first.")
                continue
            name = get_name("Name: ")
            person_id = input("ID: ").strip()
            while not person_id or len(person_id) > 20:
                print("ID is required and must be 20 characters or fewer.")
                person_id = input("ID: ").strip()
            if any(row["id"].casefold() == person_id.casefold() for row in records):
                print("That ID is already in use.")
                continue
            present = get_int("Days present: ", 0, state["total_days"])
            records.append({"name": name, "id": person_id, "present": present})
            print("Attendance record added.")
        elif choice == 3:
            print(format_attendance_report(records, state["total_days"]))
        else:
            return


def grading_menu(students):
    while True:
        print("\nGRADING SYSTEM\n1. Add student marks\n2. View report\n3. Back")
        choice = get_int("Enter choice (1-3): ", 1, 3)
        if choice == 1:
            name = get_name("Student name: ")
            marks = {subject: get_float(f"{subject} marks (0-100): ", 0, 100)
                     for subject in SUBJECTS}
            students.append({"name": name, "marks": marks})
            result = grade_student(students[-1])
            print(f"Saved. Average: {result['average']:.2f} | Grade: {result['grade']} | {result['result']}")
        elif choice == 2:
            print(format_grading_report(students))
        else:
            return


def billing_menu(invoices, state):
    while True:
        print("\nBILLING SYSTEM\n1. Create invoice\n2. View invoices\n3. Back")
        choice = get_int("Enter choice (1-3): ", 1, 3)
        if choice == 1:
            customer = get_name("Customer name: ")
            items = []
            while True:
                item_name = input("Item name (or 'done' to finish): ").strip()
                if item_name.casefold() == "done":
                    break
                if not item_name:
                    print("Item name cannot be empty.")
                    continue
                unit_price = get_float("Unit price: ", 0.01)
                quantity = get_int("Quantity: ", 1)
                items.append({"name": item_name, "unit_price": round(unit_price, 2),
                              "quantity": quantity})
            if not items:
                print("No items added; invoice was not created.")
                continue
            state["next_bill"] += 1
            bill_number = f"B{state['next_bill']:04d}"
            invoice = calculate_invoice(items)
            invoices.append({"customer": customer, "bill_number": bill_number,
                             "invoice": invoice})
            print(format_invoice(customer, bill_number, invoice))
        elif choice == 2:
            if not invoices:
                print("No invoices available.")
            for saved in invoices:
                print(format_invoice(saved["customer"], saved["bill_number"], saved["invoice"]))
                print()
        else:
            return


def reports_menu(data):
    while True:
        print("\nREPORTS\n1. Expenses\n2. Attendance\n3. Grading\n4. Billing\n5. Back")
        choice = get_int("Enter choice (1-5): ", 1, 5)
        if choice == 1:
            print(format_expense_report(data["expenses"]))
        elif choice == 2:
            print(format_attendance_report(data["attendance"], data["state"]["total_days"]))
        elif choice == 3:
            print(format_grading_report(data["students"]))
        elif choice == 4:
            if not data["invoices"]:
                print("No invoices available.")
            for saved in data["invoices"]:
                print(format_invoice(saved["customer"], saved["bill_number"], saved["invoice"]))
                print()
        else:
            return


def main():
    """Run the top-level menu; records stay in memory for this session."""
    data = {
        "expenses": [], "attendance": [], "students": [], "invoices": [],
        "state": {"total_days": 0, "next_bill": 0},
    }
    print("Integrated Expense, Attendance, Grading and Billing Manager")
    while True:
        print("\nMAIN MENU\n1. Expense Management\n2. Attendance Management"
              "\n3. Grading System\n4. Billing System\n5. View Reports\n6. Exit")
        choice = get_int("Enter choice (1-6): ", 1, 6)
        if choice == 1:
            expense_menu(data["expenses"])
        elif choice == 2:
            attendance_menu(data["attendance"], data["state"])
        elif choice == 3:
            grading_menu(data["students"])
        elif choice == 4:
            billing_menu(data["invoices"], data["state"])
        elif choice == 5:
            reports_menu(data)
        else:
            print("Thank you for using the manager. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled. Goodbye!")
