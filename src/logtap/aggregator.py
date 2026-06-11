"""
The aggregator.py module accepts parsed LogLine objects from parse_lines.py's generator, and also has access to the
global stats object to incorporate parsing stats into its own total data that will be sent to the reporter. This file's
output is a Report object which will be sent to the reporter.py module by cli.py.
"""

from typing import Iterator
from logtap.models import LogLine, ParseStats
from logtap.models import Report
from collections import Counter


def aggregate(records: Iterator[LogLine], stats: ParseStats):
    """Aggregate parsed log records into a report object for later output"""
    status_counts = [0] * 6
    total_bytes = 0
    status_other = 0

    # counters will let us do most_common(n)
    ip_counter = Counter()
    path_counter = Counter()

    timespan_start = None
    timespan_end = None

    for record in records:
        # we made status codes an int in the line parser
        if record.status_code // 100 > 1 and record.status_code // 100 < 6:
            status_counts[record.status_code // 100] += 1
        else:
            status_other += 1

        ip_counter[record.client_ip] += 1
        path_counter[record.request_uri] += 1
        total_bytes += record.response_size or 0

        if timespan_start is None:
            timespan_start = record.timestamp
            timespan_end = record.timestamp
        else:
            if record.timestamp < timespan_start:
                timespan_start = record.timestamp
            if record.timestamp > timespan_end:
                timespan_end = record.timestamp

    top_n_ips = ip_counter.most_common(5)
    top_n_paths = path_counter.most_common(5)

    report = Report(
        lines_total=stats.total,
        lines_parsed=stats.parsed,
        lines_skipped=stats.skipped,
        status_classes={
            "2xx": status_counts[2],
            "3xx": status_counts[3],
            "4xx": status_counts[4],
            "5xx": status_counts[5],
            "other": status_other,
        },
        total_bytes=total_bytes,
        top_ips=top_n_ips,
        top_paths=top_n_paths,
        timespan_start=timespan_start,
        timespan_end=timespan_end,
    )

    return report
