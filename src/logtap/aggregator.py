from logtap.models import LogLine
from logtap.models import Report
from collections import Counter
from datetime import datetime, timezone

def aggregate(records, stats):
    """Aggregate parsed log records into a report object for later output"""
    status_counts = [0] * 6
    total_bytes = 0
    status_other = 0

    # counters will let us do most_common(n)
    ip_counter = Counter()
    path_counter = Counter()

    default_date = datetime(2000, 1, 1, tzinfo=timezone.utc)
    timespan_start = default_date
    timespan_end = default_date
    first_timestamp = True

    for record in records:
        # we made status codes an int in the line parser
        if record.status_code // 100 > 1 and record.status_code // 100 < 6:
            status_counts[record.status_code // 100] += 1
        else:
            status_other += 1

        ip_counter[record.client_ip] += 1
        path_counter[record.request_uri] += 1
        total_bytes += record.response_size or 0

        if first_timestamp:
            timespan_start = record.timestamp
            timespan_end = record.timestamp
            first_timestamp = False
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
            "other": status_other
        },
        total_bytes=total_bytes,
        top_ips=top_n_ips,
        top_paths=top_n_paths,
        timespan_start=timespan_start,
        timespan_end=timespan_end
    )

    return report
