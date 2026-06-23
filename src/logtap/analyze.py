"""
The analyze module is the first step to making logtap web enabled. It takes a text stream
(or iterable of lines), runs parse + aggregate, and returns a Report. It must not print,
log policy decisions, or exit.
"""

from typing import TextIO

from logtap.aggregator import aggregate
from logtap.domain import ParseStats, Report
from logtap.parse_lines import parse_lines

def analyze(
    stream: TextIO, top_n: int
) -> Report:
    """This function takes a text stream or iterable of lines and runs parse and aggregate on them, returning a report"""

    stats = ParseStats()

    record_stream = parse_lines(stream, stats)
    stats_report = aggregate(record_stream, stats, top_n)
    return stats_report

