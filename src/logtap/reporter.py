"""
The reporter.py module is responsible for converting the Report object containing aggregated log statistics into
a printable report string.
"""

from logtap.domain import Report
import json
from dataclasses import asdict


def as_text(report: Report, top_n: int) -> str:
    """This method generates a formatted string to be output by main as the log report"""

    top_ips = "\n".join([f"  {ip}: {count}" for ip, count in report.top_ips])
    top_paths = "\n".join([f"  {path}: {count}" for path, count in report.top_paths])

    start_str = report.timespan_start.strftime("%Y-%m-%d %H:%M:%S") if report.timespan_start else "N/A"
    end_str = report.timespan_end.strftime("%Y-%m-%d %H:%M:%S") if report.timespan_end else "N/A"

    return f"""
LOGTAP REPORT
===================
Total Lines:   {report.lines_total} (Parsed: {report.lines_parsed}, Skipped: {report.lines_skipped})
Total Volume:  {report.total_bytes:,} bytes

STATUS CODES:
  2xx: {report.status_classes["2xx"]}
  3xx: {report.status_classes["3xx"]}
  4xx: {report.status_classes["4xx"]}
  5xx: {report.status_classes["5xx"]}
  other: {report.status_classes["other"]}

TOP {top_n} CLIENT IPS:
{top_ips}

TOP {top_n} REQUESTED PATHS:
{top_paths}

TIME SPAN:
  Start: {start_str}
  End:   {end_str}
  
ERROR RATE (4xx+5xx / total): {report.error_rate:.2f} %
"""

def build_dict(report: Report) -> dict:
    """This method generates a dict containing the report data"""
    payload = asdict(report)

    # add a safety check for None
    payload["timespan_start"] = report.timespan_start.isoformat() if report.timespan_start else None
    payload["timespan_end"] = report.timespan_end.isoformat() if report.timespan_end else None

    payload["error_rate"] = report.error_rate

    payload["top_ips"] = [{"ip": ip, "count": count} for ip, count in report.top_ips]
    payload["top_paths"] = [
        {"path": path, "count": count} for path, count in report.top_paths
    ]

    return payload

def as_json(report: Report) -> str:
    """This method generates a json-formatted report to be output by main as the log report"""
    output_dict = build_dict(report)

    return json.dumps(output_dict, indent=2)