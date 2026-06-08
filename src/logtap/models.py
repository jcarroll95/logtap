from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
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

@dataclass
class ParseStats:
    total: int = 0
    parsed: int = 0
    skipped: int = 0

@dataclass(frozen=True)
class Report:
    lines_total: int
    lines_parsed: int
    lines_skipped: int
    status_classes: dict[str, int]
    total_bytes: int
    top_ips: list[tuple[str, int]]
    top_paths: list[tuple[str, int]]
    timespan_start: datetime
    timespan_end: datetime

'''
1. client IP (remote host)
2. identity (almost always `-`)
3. user (almost always `-`)
4. timestamp, in square brackets, e.g. `[10/Oct/2025:13:55:36 -0700]`
5. the request line, in double quotes: HTTP method, path, protocol — e.g. `"GET /api/health HTTP/1.1"`
203.0.113.10 - - [10/Oct/2025:13:55:36 -0700] "GET /api/health HTTP/1.1" 200 512 "-" "kube-probe/1.29"
6. HTTP status code (integer)
7. response size in bytes (integer, or `-` when unknown)
8. referrer, in double quotes
9. user-agent, in double quotes

output
- **Totals:** 21 read, 19 parsed, 2 skipped
- **Status classes:** 2xx = 12, 3xx = 2, 4xx = 3, 5xx = 2, other = 0
- **Top IPs:** `203.0.113.10` = 6, then `198.51.100.23` and `192.0.2.5` tied at 4, `203.0.113.55` = 2, three more at 1
- **Top paths:** `/api/health` = 6, `/api/users` = 3, then several tied at 2
- **Total bytes:** 21663 (treating line 5's `-` as 0)
- **Time span:** 13:55:36 → 14:01:10 on 10/Oct/2025
- **Error rate** (4xx+5xx / total): 5/19 ≈ 26.3%

'''