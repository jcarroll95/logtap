import argparse
from logtap.parse_lines import parse_lines
from logtap.aggregator import aggregate
from logtap.models import ParseStats

def main():
    parser = argparse.ArgumentParser(description="The logtap CLI interface")

    parser.add_argument("filename", help="Path to log file")

    args = parser.parse_args()

    filename = args.filename
    print(filename)

    # let's define a parsing stats container
    stats = ParseStats()

    # we'll use a generator, iterating over line in file from inside parse_lines
    # to yield a record, and aggregating and iterating over the recordset in aggregator
    with open(filename, "r", encoding="utf-8") as file:
        record_stream = parse_lines(file, stats)
        # file will close when we exit the indent, so we have to stay indented
        # to keep the file openfor the generator
        record_aggregate = aggregate(record_stream, stats)

    # done with file access
    formatted_report = reporter(stats_report)
    print(formatted_report)

# this is the guard that tells python to only execute the entire file if it's being used as the main entry point
# of the program, not just having a function imported etc
if __name__ == "__main__":
    main()

    '''
    For the log file:
        cli receives file path streams lines to a list of lines
        parse_lines will parse each line from text and return python dataclass records LogLines
        aggregator will receive LogLines and compute the stats of what it receives, return stats
        reporter will take the stats and generate the report and print to stdout
    '''