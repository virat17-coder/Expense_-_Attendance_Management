# Integrated Expense, Attendance, Grading and Billing Manager

A menu-driven Python 3.8+ console program based on the supplied requirements. It uses only the Python standard library. Records are kept in memory and are cleared when the program exits.

## Run it

```text
python main.py
```

Choose a module from the main menu, then follow the prompts. The expense categories are Food, Travel, Utilities, Stationery, and Other. Attendance status is Eligible at 75% or higher, Warning from 60% to below 75%, and Shortage below 60%. Grading uses five subjects by default; any subject mark below 35 means the student fails, even if the average is higher.

Bills use the specified subtotal discounts (5% from 1,000; 10% from 5,000; 15% from 10,000), then calculate 18% tax on the discounted taxable amount. Monetary figures are rounded to two decimal places.

## Modules

- Expense management: add expenses, view totals by category, grand total, and highest/lowest expense.
- Attendance: set working days, record a person's attendance, and view individual and class summaries.
- Grading: record marks for Maths, Science, English, Computer, and History; view grades and class pass/fail totals.
- Billing: create itemized invoices, apply discounts and tax, and view saved invoices.
- Reports: open the report for any module.

The implementation is kept in `main.py` so it is straightforward to run and review. Reusable functions near the top perform validation, calculations, and report formatting; menu functions handle user input.

## Run the test cases

```text
python -m unittest discover -s tests -v
```

The test log is in `TEST_LOG.md`. See `SAMPLE_OUTPUT.md` for an example invoice and report.
