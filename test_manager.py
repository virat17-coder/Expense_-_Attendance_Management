import unittest

import main


class CalculationTests(unittest.TestCase):
    def test_grade_90_is_a_plus(self):
        self.assertEqual(main.grade_for(90), "A+")

    def test_grade_89_99_is_a(self):
        self.assertEqual(main.grade_for(89.99), "A")

    def test_grade_80_is_a(self):
        self.assertEqual(main.grade_for(80), "A")

    def test_grade_70_is_b(self):
        self.assertEqual(main.grade_for(70), "B")

    def test_grade_60_is_c(self):
        self.assertEqual(main.grade_for(60), "C")

    def test_grade_50_is_d(self):
        self.assertEqual(main.grade_for(50), "D")

    def test_grade_35_is_e(self):
        self.assertEqual(main.grade_for(35), "E")

    def test_grade_below_35_is_f(self):
        self.assertEqual(main.grade_for(34.99), "F")

    def test_attendance_75_is_eligible(self):
        self.assertEqual(main.attendance_status(75), "Eligible")

    def test_attendance_60_is_warning(self):
        self.assertEqual(main.attendance_status(60), "Warning")

    def test_attendance_below_60_is_shortage(self):
        self.assertEqual(main.attendance_status(59.99), "Shortage")

    def test_attendance_summary_counts_statuses(self):
        rows = [{"name": "Asha", "id": "1", "present": 8},
                {"name": "Ravi", "id": "2", "present": 6},
                {"name": "Mina", "id": "3", "present": 5}]
        summary = main.attendance_summary(rows, 10)
        self.assertEqual(summary["counts"], {"Eligible": 1, "Warning": 1, "Shortage": 1})

    def test_discount_below_first_slab(self):
        self.assertEqual(main.discount_rate(999.99), 0)

    def test_discount_first_boundary(self):
        self.assertEqual(main.discount_rate(1000), .05)

    def test_discount_second_boundary(self):
        self.assertEqual(main.discount_rate(5000), .10)

    def test_discount_top_boundary(self):
        self.assertEqual(main.discount_rate(10000), .15)

    def test_invoice_tax_is_after_discount(self):
        result = main.calculate_invoice([{"name": "Book", "unit_price": 1000, "quantity": 1}])
        self.assertEqual(result["discount"], 50)
        self.assertEqual(result["taxable"], 950)
        self.assertEqual(result["tax"], 171)
        self.assertEqual(result["total"], 1121)

    def test_invoice_rounds_line_items(self):
        result = main.calculate_invoice([{"name": "Item", "unit_price": 1.336, "quantity": 3}])
        self.assertEqual(result["items"][0]["line_total"], 4.01)

    def test_student_fails_if_one_subject_below_35(self):
        student = {"name": "Asha", "marks": {"M": 34, "S": 90}}
        self.assertEqual(main.grade_student(student)["result"], "FAIL")

    def test_student_passes_when_all_subjects_at_least_35(self):
        student = {"name": "Asha", "marks": {"M": 35, "S": 90}}
        self.assertEqual(main.grade_student(student)["result"], "PASS")

    def test_empty_expense_summary_is_safe(self):
        result = main.expense_summary([])
        self.assertEqual(result["grand_total"], 0)
        self.assertIsNone(result["highest"])

    def test_empty_reports_show_no_data_message(self):
        self.assertIn("No expense records", main.format_expense_report([]))
        self.assertIn("No student records", main.format_grading_report([]))

    def test_expense_category_totals(self):
        rows = [{"description": "Bus", "category": "Travel", "amount": 20.25},
                {"description": "Train", "category": "Travel", "amount": 9.75}]
        self.assertEqual(main.expense_summary(rows)["category_totals"]["Travel"], 30)


if __name__ == "__main__":
    unittest.main()
