import io
from logtap.parse_lines import parse_lines
from logtap.models import ParseStats

def test_parse_lines_valid_input():
    """This test asserts that parse_lines correctly extracts fields from valid log lines"""
    #arrange
    raw_logs = (
        '203.0.113.10 - - [10/Oct/2025:13:55:36 -0700] "GET /api HTTP/1.1" 200 512 "-" "agent"\n'
        '192.0.2.1 - - [10/Oct/2025:13:56:00 -0700] "POST /login HTTP/1.1" 404 - "-" "agent"\n'
    )
    mock_file = io.StringIO(raw_logs)
    stats = ParseStats()

    #act
    records = list(parse_lines(mock_file, stats))

    #assert
    assert stats.total == 2


def test_parse_lines_bad_lines():
    """This test asserts that parse_lines skips processing lines with no regex match"""
    #arrange
    raw_logs = (
        'this is the first bad log line\n'
        '- - - - - - - - - - - - - "\n'
    )
    mock_file = io.StringIO(raw_logs)
    stats = ParseStats()

    #act
    records = list(parse_lines(mock_file, stats))

    #assert
    assert stats.total == 2
    assert stats.skipped == 2


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
    assert records[0].response_size == None
    assert records[1].response_size == None
