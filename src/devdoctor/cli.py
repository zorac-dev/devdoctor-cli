import argparse

from devdoctor.checks.system import get_system_info
from devdoctor.checks.tools import check_git
from devdoctor.models import Status
from devdoctor.report import print_report


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="devdoctor",
        description="Developer environment diagnostic tool",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="devdoctor 0.1.0",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "check",
        help="Check developer environment",
    )

    args = parser.parse_args()

    if args.command == "check":
        system_info = get_system_info()
        results = [check_git()]

        print_report(system_info, results)

        if any(r.status == Status.ERROR for r in results):
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
