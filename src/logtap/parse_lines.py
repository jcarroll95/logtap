import re
from logtap.models import LogLine
from datetime import datetime

def parse_lines(file, stats):
    # This regex pattern looks for:
    # 1. Non-whitespace (\S+)
    # 2. Bracketed content \[(.*?)\]
    # 3. Quoted content "(.*?)"
    # 4. Integers (\d+)
    LOG_PATTERN = re.compile(
        r'(?P<ip>\S+) '
        r'(?P<identity>\S+) '
        r'(?P<user>\S+) '
        r'\[(?P<timestamp>.*?)\] '
        r'"(?P<method>\S+) (?P<uri>\S+) (?P<protocol>\S+)" '
        r'(?P<status>\d+) '
        r'(?P<size>\S+) '
        r'"(?P<referrer>.*?)" '
        r'"(?P<agent>.*?)"'
    )

    for line in file:
        stats.total += 1
        match = LOG_PATTERN.match(line.strip())
        if not match:
            return None

        data = match.groupdict()

        # 1. Parse the timestamp
        # Format: 10/Oct/2025:13:55:36 -0700
        ts = datetime.strptime(data['timestamp'], "%d/%b/%Y:%H:%M:%S %z")
        # 2. Handle the "size" which might be "-"
        size = int(data['size']) if data['size'].isdigit() else None
        # 3. Create the record
        record = LogLine(
            client_ip=data['ip'],
            identity=data['identity'],
            user=data['user'],
            timestamp=ts,
            request_method=data['method'],
            request_uri=data['uri'],
            request_protocol=data['protocol'],
            status_code=int(data['status']),
            response_size=size,
            referrer=data['referrer'],
            user_agent=data['agent']
        )
        if record:
            stats.parsed += 1
            yield record
        else:
            stats.skipped += 1


'''
class LogLine:
    client_ip: str
    identity: str
    user: str
    timestamp: datetime
    request_method: str
    request_uri: str
    request_protocol: str
    status_code: int
    response_size: int | None
    referrer: str
    user_agent: str


203.0.113.10 - - [10/Oct/2025:13:55:36 -0700] "GET /api/health HTTP/1.1" 200 512 "-" "kube-probe/1.29"
'''