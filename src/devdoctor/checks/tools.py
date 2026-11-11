import re
import shutil
import subprocess
import sys

from devdoctor.models import CheckResult, Status

# Diagnostic targets
TOOLS = {
    "Git": ["git", "--version"],
    "uv": ["uv", "--version"],
    "Docker": ["docker", "--version"],
    "fzf": ["fzf", "--version"],
}


def extract_version(output: str) -> str | None:
    """Extract a version number from command output."""
    match = re.search(
        r"\b\d+\.\d+(?:\.\d+)*(?:[-+][0-9A-Za-z.-]+)?",
        output,
    )
    return match.group(0) if match else None


def check_tool(
    name: str,
    command: list[str],
) -> CheckResult:
    """Check an external development tool."""
    if not command:
        return CheckResult(
            name=name,
            status=Status.ERROR,
            message="No command specified",
        )

    if shutil.which(command[0]) is None:
        return CheckResult(
            name=name,
            status=Status.MISSING,
            message="Not installed",
        )

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )

        output = result.stdout.strip() or result.stderr.strip()
        version = extract_version(output)

        return CheckResult(
            name=name,
            status=Status.OK,
            version=version,
            message=None if version else "Version unknown",
        )

    except (subprocess.SubprocessError, OSError) as exc:
        return CheckResult(
            name=name,
            status=Status.ERROR,
            message=str(exc),
        )


def check_python() -> CheckResult:
    """Check the current Python interpreter."""
    version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    return CheckResult(
        name="Python",
        status=Status.OK,
        version=version,
    )


def check_git() -> CheckResult:
    """Check Git. Kept for compatibility with existing tests."""
    return check_tool("Git", TOOLS["Git"])


def check_development_tools() -> list[CheckResult]:
    """Run all development tool checks."""
    results = [check_python()]

    for name, command in TOOLS.items():
        results.append(check_tool(name, command))

    return results
