import shutil
import subprocess

from devdoctor.models import CheckResult, Status


def check_tool(
    name: str,
    command: list[str],
) -> CheckResult:
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

        return CheckResult(
            name=name,
            status=Status.OK,
            version=output.splitlines()[0] if output else None,
        )

    except (subprocess.SubprocessError, OSError) as exc:
        return CheckResult(
            name=name,
            status=Status.ERROR,
            message=str(exc),
        )


def check_git() -> CheckResult:
    result = check_tool("Git", ["git", "--version"])

    if result.status == Status.OK and result.version:
        version = result.version.removeprefix("git version ").strip()
        return CheckResult(
            name="Git",
            status=Status.OK,
            version=version,
        )

    return result
