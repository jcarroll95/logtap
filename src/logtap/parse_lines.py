"""
parse_lines.py is meant to accept a file stream and a global stats object as inputs, and use a generator to iterate over the file
stream per line to separate valid log line fields, validate minimum required data, and construct a LogLine record
object to be passed to the aggregator.py which aggregates and processes the data objects. The stats object is used to
track total, skipped, and parsed log lines.
"""

from typing import TextIO, Any, Generator
import re
import logging
import ipaddress
from logtap.models import LogLine, ParseStats
from datetime import datetime


def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def parse_lines(file: TextIO, stats: ParseStats, quiet: bool) -> Generator[LogLine, Any, None]:
    """Parse log lines from a given file into record objects for aggregation"""
    logger = logging.getLogger(__name__)

    # This regex pattern looks for:
    # 1. Non-whitespace (\S+)
    # 2. Bracketed content \[(.*?)\]
    # 3. Quoted content "(.*?)"
    # 4. Integers (\d+)
    LOG_PATTERN = re.compile(
        r"(?P<ip>\S+) "
        r"(?P<identity>\S+) "
        r"(?P<user>\S+) "
        r"\[(?P<timestamp>.*?)\] "
        r'"(?P<method>\S+) (?P<uri>\S+) (?P<protocol>\S+)" '
        r"(?P<status>\d+) "
        r"(?P<size>\S+) "
        r'"(?P<referrer>.*?)" '
        r'"(?P<agent>.*?)"'
    )

    """
    Let's establish the minimum fields required for a valid log line:
    - IP address must be present and not malformed (who)
    - Timestamp must be enclosed in [], and parseable as a datetime object (when)
    - Request method, URI, and protocol must be present (what)
    - Status code must be present and parseable as an integer (result)
    
    Not required:
    - RFC 1413 identity and User ID
    - Response size
    - referrer/user agent
    """

    for line in file:
        stats.total += 1
        match = LOG_PATTERN.match(line.strip())
        if not match:
            if not quiet:
                logger.warning(f"Skipping bad log line: \n{line.strip()}")
            stats.skipped += 1
            continue

        data = match.groupdict()

        # validate the ip address string
        if not is_valid_ip(data["ip"]):
            stats.skipped += 1
            continue

        # validate the timestamp string
        try:
            # Format: 10/Oct/2025:13:55:36 -0700
            ts = datetime.strptime(data["timestamp"], "%d/%b/%Y:%H:%M:%S %z")
        except ValueError:
            if not quiet:
                logger.warning(f"Skipping line with bad timestamp:  \n{line.strip()}")
            stats.skipped += 1
            continue

        # validate request method, uri, protocol present
        if not data["method"] or not data["uri"] or not data["protocol"]:
            if not quiet:
                logger.warning(f"Skipping line with missing fields for method, uri, or protocol: \n{line.strip()}")
            stats.skipped += 1
            continue

        # validate the status code is present and an integer
        if data["status"].isdigit():
            status = int(data["status"])
        else:
            if not quiet:
                logger.warning(f"Skipping line with bad status code: \n{line.strip()}")
            stats.skipped += 1
            continue

        # handle the "size" which might be "-", and validate status
        size = int(data["size"]) if data["size"].isdigit() else None

        # create the record
        record = LogLine(
            client_ip=data["ip"],
            identity=data["identity"],
            user=data["user"],
            timestamp=ts,
            request_method=data["method"],
            request_uri=data["uri"],
            request_protocol=data["protocol"],
            status_code=status,
            response_size=size,
            referrer=data["referrer"],
            user_agent=data["agent"],
        )

        # we made it here, so the record is valid
        stats.parsed += 1
        yield record
