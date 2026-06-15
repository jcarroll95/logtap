"""
The cli.py file contains our program's CLI interface. It accepts a file path argument and runs
the analyze module to produce a report object, then the reporter module to produce a formatted
printable report of those objects
"""

import argparse
import sys
import logging
from logtap.reporter import as_json, as_text
from logtap.analyze import analyze

def main():
    """The CLI main interface: accept arguments and run logtap on the specified file"""

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

    # If quiet, only show CRITICAL errors. Otherwise, show everything from INFO up.
    log_level = logging.CRITICAL if args.quiet else logging.INFO

    # Set up the internal app log, root logger
    logging.basicConfig(
        # filename="logtap.log",
        # filemode="a",  # 'a' to append, 'w' to overwrite
        level=log_level,  # Capture INFO and more severe logs
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.info(f"Filename argument received: {filename}")

    # CLI is now just an interface to use the analyze service
    logging.info(f"Opening {filename} file...")
    stats_report = analyze(args.file, top_n=args.top)
    if args.file is not sys.stdin:
        args.file.close()
    logging.info(f"{filename} file closed.")

    # done with file access
    if args.json:
        formatted_report = as_json(stats_report)
    else:
        formatted_report = as_text(stats_report, top_n=args.top)
    print(formatted_report)

    sys.exit(0)

# this is the guard that tells python to only execute the entire file if it's being used as the main entry point
# of the program, not just having a function imported etc
if __name__ == "__main__":
    main()
