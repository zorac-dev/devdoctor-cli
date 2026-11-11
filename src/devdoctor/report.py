from collections import Counter

from devdoctor.models import CheckResult, Status


def print_report(
    system_info: dict[str, str],
    results: list[CheckResult],
) -> None:
    print("devdoctor v0.1.0")
    print("─" * 32)

    print("SYSTEM")
    print(f"  OS       {system_info['os']}")
    print(f"  Arch     {system_info['arch']}")
    print()

    print("DEVELOPMENT TOOLS")

    for result in results:
        detail = result.version or result.message or ""
        print(f"  {result.name:<8} {result.status.value.upper():<8} {detail}")

    print("─" * 32)

    counts = Counter(result.status for result in results)

    print(
        f"{counts[Status.OK]} installed / "
        f"{counts[Status.MISSING]} missing / "
        f"{counts[Status.ERROR]} errors"
    )
