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
from logtap.reporter import as_json, as_text


def main():
    """The CLI main interface: accept arguments and run logtap on the specified file"""

    # Set up the internal app log, root logger
    logging.basicConfig(
        # filename="logtap.log",
        # filemode="a",  # 'a' to append, 'w' to overwrite
        level=logging.INFO,  # Capture INFO and more severe logs
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Set up the CLI argument parser
    parser = argparse.ArgumentParser(
        prog="LogTap",
        description="LogTap is a Common Log Format (CLF) parser and reporter",
        epilog="uv run logtap <filename> to run",
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Path to log file (defaults to stdin if omitted)",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output in JSON format (defaults to string)",
    )
    parser.add_argument(
        "-t",
        "--top",
        type=int,
        default=5,
        help="Number of IPs and paths to include in the Top N (defaults to 5)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress line skip warnings. Quiet is off by default.",
    )

    args = parser.parse_args()
    filename = args.file.name
    if not args.quiet:
        logging.info(f"Filename argument received: {filename}")

    # Define a parsing stats container
    stats = ParseStats()

    # we'll use a generator, iterating over line in file from inside parse_lines
    # to yield a record, and aggregating and iterating over the recordset in aggregator
    if not args.quiet:
        logging.info(f"Opening {filename} file...")
    record_stream = parse_lines(args.file, stats, quiet=args.quiet)
    stats_report = aggregate(record_stream, stats, top_n=args.top)
    args.file.close()
    if not args.quiet:
        logging.info(f"{filename} file closed.")

    # done with file access
    if args.json:
        formatted_report = as_json(stats_report, top_n=args.top)
    else:
        formatted_report = as_text(stats_report, top_n=args.top)
    print(formatted_report)

    sys.exit(0)


# this is the guard that tells python to only execute the entire file if it's being used as the main entry point
# of the program, not just having a function imported etc
if __name__ == "__main__":
    main()
