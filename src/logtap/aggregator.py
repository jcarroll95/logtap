from logtap.models import LogLine


'''
Aggregator takes generator-given records (LogLine) from parse_lines
and builds the in-memory stats to return
- total lines read, total parsed, total skipped
- count of requests by status class: 2xx, 3xx, 4xx, 5xx, and "other"
- top N requested paths by count
- top N client IPs by count
- total bytes transferred

stats input:
- total lines read
- total lines parsed
- total lines skipped

stats DERIVED:
- counts by status class
- top N requested paths by count
- top N client IPs by count
- total bytes transferred


'''
def aggregate(records, stats):
    for record in records:

