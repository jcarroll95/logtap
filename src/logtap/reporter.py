"""
The reporter.py module is responsible for converting the Report object containing aggregated log statistics into
a printable report string.
"""

from logtap.models import Report


def reporter(report: Report):

    top_ips = "\n".join([f"  {ip}: {count}" for ip, count in report.top_ips])
    top_paths = "\n".join([f"  {path}: {count}" for path, count in report.top_paths])

    if report.lines_total == 0:
        error_rate = 0
    else:
        error_rate = (
            (report.status_classes["4xx"] + report.status_classes["5xx"])
            / report.lines_parsed
            * 100
        )
    error_rate = round(error_rate, 2)

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

TOP 5 CLIENT IPS:
{top_ips}

TOP 5 REQUESTED PATHS:
{top_paths}

TIME SPAN:
  Start: {report.timespan_start:%Y-%m-%d %H:%M:%S}
  End:   {report.timespan_end:%Y-%m-%d %H:%M:%S}
  
ERROR RATE (4xx+5xx / total): {error_rate:.2f} %
"""
