import io
from logtap.parse_lines import parse_lines
from logtap.models import ParseStats
import datetime


def test_parse_lines_valid_input():
    """This test asserts that parse_lines correctly extracts fields from valid log lines"""
    # arrange
    raw_logs = (
        '203.0.113.10 - - [10/Oct/2025:13:55:36 -0700] "GET /api HTTP/1.1" 200 512 "-" "agent"\n'
        '192.0.2.1 - - [10/Oct/2025:13:56:00 -0700] "POST /login HTTP/1.1" 404 - "-" "agent"\n'
    )
    mock_file = io.StringIO(raw_logs)
    stats = ParseStats()

    # act
    records = list(parse_lines(mock_file, stats))

    # assert
    assert stats.total == 2
    assert len(records) == 2
    assert records[0].client_ip == "203.0.113.10"
    assert records[0].timestamp == datetime.datetime(
        2025,
        10,
        10,
        13,
        55,
        36,
        tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200)),
    )
    assert records[0].request_method == "GET"
    assert records[0].request_uri == "/api"
    assert records[0].request_protocol == "HTTP/1.1"
    assert records[0].status_code == 200
    assert records[0].response_size == 512
    assert records[0].referrer == "-"
    assert records[0].user_agent == "agent"
    assert records[1].client_ip == "192.0.2.1"
    assert records[1].timestamp == datetime.datetime(
        2025,
        10,
        10,
        13,
        56,
        00,
        tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200)),
    )
    assert records[1].request_method == "POST"
    assert records[1].request_uri == "/login"
    assert records[1].request_protocol == "HTTP/1.1"
    assert records[1].status_code == 404
    assert records[1].response_size is None
    assert records[1].referrer == "-"
    assert records[1].user_agent == "agent"


def test_parse_lines_bad_lines():
    """This test asserts that parse_lines skips processing lines that fail the validation criteria:
    - regex match
    - IP address must be present and not malformed (who)
    - Timestamp must be enclosed in [], and parseable as a datetime object (when)
    - Request method, URI, and protocol must be present (what)
    - Status code must be present and parseable as an integer (result)"""
    # arrange
    raw_logs = (
        "this is the first bad log line\n"
        '- - - - - - - - - - - - - "\n'
        '203.0.113.x - - [10/Oct/2025:13:55:36 -0700] "GET /api HTTP/1.1" 200 512 "-" "agent"\n'
        '192.0.2.1 - - [17/Fri/20205:13:56:00 -0700] "POST /login HTTP/1.1" 404 - "-" "agent"\n'
        '203.0.113.10 - - [10/Oct/2025:13:55:36 -0700] "/api HTTP/1.1" 200 512 "-" "agent"\n'
        '203.0.113.10 - - [10/Oct/2025:13:55:36 -0700] "GET /api HTTP/1.1" 5XX 512 "-" "agent"\n'
    )
    mock_file = io.StringIO(raw_logs)
    stats = ParseStats()

    # act
    records = list(parse_lines(mock_file, stats))

    # assert
    assert records == []
    assert stats.total == 6
    assert stats.skipped == 6


def test_parse_lines_bad_size():
    """This test ensures that response_size is correctly converted to None"""
    raw_logs = (
        '203.0.113.10 - - [10/Oct/2025:13:55:36 -0700] "GET /api HTTP/1.1" 200 - "-" "agent"\n'
        '192.0.2.1 - - [10/Oct/2025:13:56:00 -0700] "POST /login HTTP/1.1" 404 -64 "-" "agent"\n'
    )
    mock_file = io.StringIO(raw_logs)
    stats = ParseStats()

    records = list(parse_lines(mock_file, stats))

    assert stats.total == 2
    assert records[0].response_size is None
    assert records[1].response_size is None
