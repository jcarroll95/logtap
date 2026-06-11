"""
The reporter.py module is responsible for converting the Report object containing aggregated log statistics into
a printable report string.
"""

from logtap.models import Report


def reporter(report: Report, top_n: int) -> str:
    """This method generates a formatted string to be output by main as the log report"""

    top_ips = "\n".join([f"  {ip}: {count}" for ip, count in report.top_ips])
    top_paths = "\n".join([f"  {path}: {count}" for path, count in report.top_paths])

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
  Start: {report.timespan_start:%Y-%m-%d %H:%M:%S}
  End:   {report.timespan_end:%Y-%m-%d %H:%M:%S}
  
ERROR RATE (4xx+5xx / total): {report.error_rate:.2f} %
"""
