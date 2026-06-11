from logtap.models import LogLine, ParseStats
from logtap.aggregator import aggregate
from datetime import datetime, timezone


def test_aggregate_counts_correctly():
    """Test that aggregation logic correctly calculates stats for report"""
    # Arrange: Create a few mock log records
    stats = ParseStats()
    records = [
        LogLine(
            "1.1.1.1",
            "-",
            "-",
            datetime.now(timezone.utc),
            "GET",
            "/",
            "HTTP/1.1",
            200,
            100,
            "-",
            "-",
        ),
        LogLine(
            "1.1.1.1",
            "-",
            "-",
            datetime.now(timezone.utc),
            "GET",
            "/",
            "HTTP/1.1",
            404,
            50,
            "-",
            "-",
        ),
    ]
    # Update stats manually as parse_lines would
    stats.total = 2
    stats.parsed = 2

    # Act: Run the aggregation logic
    report = aggregate(records, stats)

    # Assert: Verify the results
    # Status codes are correctly grouped
    assert report.status_classes["2xx"] == 1
    assert report.status_classes["4xx"] == 1
    # Total bytes is calculated correctly
    assert report.total_bytes == 150
    # Top IPs and top paths are sorted correctly
    assert report.top_ips[0] == ("1.1.1.1", 2)
    assert report.top_paths[0] == ("/", 2)
    # The timespan correctly identifies the earliest and latest timestamps
    assert report.timespan_start == records[0].timestamp
    assert report.timespan_end == records[1].timestamp
