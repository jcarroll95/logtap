"""
3. Error Rate Calculation & Empty File Handling (src/logtap/reporter.py)
•
Why: The reporter performs a critical calculation for the ERROR RATE. Division by zero is
a common risk if a log file is empty or all lines are skipped.
•
What to test:
◦
Calculation: Verify the math for (4xx + 5xx) / total.
◦
Safety: Pass a Report object with lines_total = 0 to ensure the reporter returns 0.00%
rather than crashing with a ZeroDivisionError.
"""
