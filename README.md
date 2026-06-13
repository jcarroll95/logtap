# LogTap 🚰

LogTap is a lightweight CLI tool written in Python for parsing and analyzing Common Log Format (CLF) files. It processes logs streamingly to maintain a low memory footprint even with large files.

## Features
- **Streaming Parser**: Processes logs line-by-line using Python generators.
- **CLF Support**: Handles standard web server logs including quoted strings and timestamps.
- **Summary Reports**: Generates statistics on status codes, volume, and top client IPs/paths.

## Installation
Ensure you have [uv](https://github.com/astral-sh/uv) installed.

```bash
git clone <repository-url>
cd logtap
uv sync
```

## Usage

### Analyze a log file
```bash
uv run logtap access.log
```

### Stream from stdin
```bash
cat access.log | uv run logtap
```

### Example Output
```text
LOGTAP REPORT
===================
Total Lines:   21 (Parsed: 19, Skipped: 2)
Total Volume:  21,663 bytes

STATUS CODES:
  2xx: 12
  3xx: 2
  4xx: 3
  5xx: 2
  other: 0

TOP 5 CLIENT IPS:
  203.0.113.10: 6
  198.51.100.23: 4
  192.0.2.5: 4
  203.0.113.55: 2
  198.51.100.99: 1

TOP 5 REQUESTED PATHS:
  /api/health: 6
  /api/users: 3
  /index.html: 2
  /api/login: 2
  /static/app.css: 2

TIME SPAN:
  Start: 2025-10-10 13:55:36
  End:   2025-10-10 14:01:10
  
ERROR RATE (4xx+5xx / total): 26.32 %
```
