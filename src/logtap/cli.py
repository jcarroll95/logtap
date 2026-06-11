"""
The cli.py file contains our programs main entrypoint and interface. It accepts a file path argument and runs
the sequence of parse_lines, aggragator, and reporter to translate log file data into memory objects and produce
a printable report of those objects
"""

import argparse
import sys
import logging
from logtap.parse_lines import parse_lines
from logtap.aggregator import aggregate
from logtap.models import ParseStats
from logtap.reporter import reporter


def main():
    """The CLI main interface: accept arguments and run logtap on the specified file"""

    # Set up the internal app log, root logger
    logging.basicConfig(
        filename="logtap.log",
        filemode="a",  # 'a' to append, 'w' to overwrite
        level=logging.INFO,  # Capture INFO and more severe logs
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Set up the CLI argument parser
    parser = argparse.ArgumentParser(
        prog="LogTap",
        description="LogTap is a Common Log Format (CLF) parser and reporter",
        epilog="try"
    )
    parser.add_argument("filename", type=str, help="Path to log file")
    args = parser.parse_args()
    filename = args.filename
    logging.info(f"Filename argument received: {filename}")

    # Define a parsing stats container
    stats = ParseStats()

    # we'll use a generator, iterating over line in file from inside parse_lines
    # to yield a record, and aggregating and iterating over the recordset in aggregator
    try:
        logging.info(f"Opening {filename} file...")
        with open(filename, "r", encoding="utf-8") as file:
            record_stream = parse_lines(file, stats)
            # file will close when we exit the indent, so we have to stay indented
            # to keep the file openfor the generator
            stats_report = aggregate(record_stream, stats)
        logging.info(f"{filename} file closed.")
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        print(f"File not found: {filename}\n", file=sys.stderr)
        sys.exit(2)

    # done with file access
    formatted_report = reporter(stats_report)
    print(formatted_report)

    sys.exit(0)


# this is the guard that tells python to only execute the entire file if it's being used as the main entry point
# of the program, not just having a function imported etc
if __name__ == "__main__":
    main()
