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

from logtap.models import Report
from logtap.reporter import as_text, as_json
import datetime


def test_reporter_calculation():
    """This test asserts that reporter correctly calculates the error rate"""
    # arrange
    report = Report(
        lines_total=10,
        lines_parsed=10,
        lines_skipped=0,
        status_classes={
            "2xx": 3,
            "3xx": 3,
            "4xx": 2,
            "5xx": 2,
            "other": 0,
        },
        total_bytes=0,
        top_ips=[],
        top_paths=[],
        timespan_start=datetime.datetime.now(),
        timespan_end=datetime.datetime.now(),
    )

    # act
    output_string = as_text(report, 5)
    expected_string_value = f"{report.error_rate:.2f} %"

    # assert
    assert report.error_rate == 40.00
    assert expected_string_value in output_string


def test_reporter_empty_file():
    """This test asserts that the report doesn't error from 0 lines or divide by zero"""
    # arrange
    report = Report(
        lines_total=0,
        lines_parsed=0,
        lines_skipped=0,
        status_classes={
            "2xx": 0,
            "3xx": 0,
            "4xx": 0,
            "5xx": 0,
            "other": 0,
        },
        total_bytes=0,
        top_ips=[],
        top_paths=[],
        timespan_start=datetime.datetime.min,
        timespan_end=datetime.datetime.min,
    )

    # act
    output_string = as_text(report, 5)
    expected_string_value = f"{report.error_rate:.2f} %"

    # assert
    assert report.error_rate == 0.00
    assert expected_string_value in output_string


def test_reporter_json_calculation():
    """This test asserts that reporter correctly calculates the error rate"""
    # arrange
    report = Report(
        lines_total=10,
        lines_parsed=10,
        lines_skipped=0,
        status_classes={
            "2xx": 3,
            "3xx": 3,
            "4xx": 2,
            "5xx": 2,
            "other": 0,
        },
        total_bytes=0,
        top_ips=[],
        top_paths=[],
        timespan_start=datetime.datetime.now(),
        timespan_end=datetime.datetime.now(),
    )

    # act
    output_payload = as_json(report, 5)
    expected_json_value = f"{report.error_rate:.1f}"

    # assert
    assert report.error_rate == 40.00
    assert expected_json_value in output_payload


def test_reporter_json_empty_file():
    """This test asserts that the report doesn't error from 0 lines or divide by zero"""
    # arrange
    report = Report(
        lines_total=0,
        lines_parsed=0,
        lines_skipped=0,
        status_classes={
            "2xx": 0,
            "3xx": 0,
            "4xx": 0,
            "5xx": 0,
            "other": 0,
        },
        total_bytes=0,
        top_ips=[],
        top_paths=[],
        timespan_start=datetime.datetime.min,
        timespan_end=datetime.datetime.min,
    )

    # act
    output_payload = as_json(report, 5)
    expected_json_value = f"{report.error_rate:.1f}"

    # assert
    assert report.error_rate == 0.00
    assert expected_json_value in output_payload
