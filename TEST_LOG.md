# Test log

Command run: `python -m unittest discover -s tests -v`  
Result: **23 tests passed, 0 failed**.

| ID | Area | Check | Result |
|---|---|---|---|
| TC-01 | Grading | 90 maps to A+ | Pass |
| TC-02 | Grading | 89.99 maps to A | Pass |
| TC-03 | Grading | 80 maps to A | Pass |
| TC-04 | Grading | 70 maps to B | Pass |
| TC-05 | Grading | 60 maps to C | Pass |
| TC-06 | Grading | 50 maps to D | Pass |
| TC-07 | Grading | 35 maps to E | Pass |
| TC-08 | Grading | Below 35 maps to F | Pass |
| TC-09 | Attendance | 75% is Eligible | Pass |
| TC-10 | Attendance | 60% is Warning | Pass |
| TC-11 | Attendance | Below 60% is Shortage | Pass |
| TC-12 | Attendance | Summary counts each status | Pass |
| TC-13 | Billing | Below 1,000 has no discount | Pass |
| TC-14 | Billing | 1,000 subtotal gets 5% discount | Pass |
| TC-15 | Billing | 5,000 subtotal gets 10% discount | Pass |
| TC-16 | Billing | 10,000 subtotal gets 15% discount | Pass |
| TC-17 | Billing | Tax is calculated after discount | Pass |
| TC-18 | Billing | Line total is rounded to two decimals | Pass |
| TC-19 | Grading | Student fails when one subject is below 35 | Pass |
| TC-20 | Grading | Student passes when all subject marks are at least 35 | Pass |
| TC-21 | Expenses | Empty report handles no records | Pass |
| TC-22 | Reports | Empty grading report handles no records | Pass |
| TC-23 | Expenses | Multiple expenses add to the category total | Pass |

These automated checks cover calculation boundaries and empty-record cases. Manual menu testing should still be done on the target computer before a live demonstration.
