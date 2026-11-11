import subprocess
import sys
from unittest.mock import patch

import pytest

from devdoctor.checks.tools import (
    check_development_tools,
    check_git,
    check_python,
    check_tool,
    extract_version,
)
from devdoctor.models import CheckResult, Status


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        ("git version 2.47.0", "2.47.0"),
        ("uv 0.9.0 (abc123)", "0.9.0"),
        ("Docker version 29.0.0, build abc", "29.0.0"),
        ("0.65.0 (abcdef)", "0.65.0"),
        ("not a version", None),
    ],
)
def test_extract_version(output, expected):
    assert extract_version(output) == expected


def test_python_version():
    result = check_python()

    expected = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    assert result.name == "Python"
    assert result.status == Status.OK
    assert result.version == expected


def test_tool_installed():
    with (
        patch(
            "devdoctor.checks.tools.shutil.which",
            return_value="/usr/bin/docker",
        ),
        patch(
            "devdoctor.checks.tools.subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=["docker", "--version"],
                returncode=0,
                stdout="Docker version 29.0.0, build abc\n",
                stderr="",
            ),
        ),
    ):
        result = check_tool(
            "Docker",
            ["docker", "--version"],
        )

    assert result.status == Status.OK
    assert result.version == "29.0.0"


def test_tool_missing():
    with patch(
        "devdoctor.checks.tools.shutil.which",
        return_value=None,
    ):
        result = check_tool(
            "Docker",
            ["docker", "--version"],
        )

    assert result.status == Status.MISSING


def test_tool_error():
    with (
        patch(
            "devdoctor.checks.tools.shutil.which",
            return_value="/usr/bin/docker",
        ),
        patch(
            "devdoctor.checks.tools.subprocess.run",
            side_effect=subprocess.CalledProcessError(
                returncode=1,
                cmd=["docker", "--version"],
            ),
        ),
    ):
        result = check_tool(
            "Docker",
            ["docker", "--version"],
        )

    assert result.status == Status.ERROR


def test_all_development_tools():
    with patch(
        "devdoctor.checks.tools.check_tool",
        side_effect=lambda name, command: CheckResult(
            name=name,
            status=Status.OK,
            version="1.0.0",
        ),
    ):
        results = check_development_tools()

    names = [result.name for result in results]

    assert names == [
        "Python",
        "Git",
        "uv",
        "Docker",
        "fzf",
    ]


def test_git_installed():
    with (
        patch(
            "devdoctor.checks.tools.shutil.which",
            return_value="/usr/bin/git",
        ),
        patch(
            "devdoctor.checks.tools.subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=["git", "--version"],
                returncode=0,
                stdout="git version 2.47.0\n",
                stderr="",
            ),
        ),
    ):
        result = check_git()

    assert result.status == Status.OK
    assert result.version == "2.47.0"


def test_git_missing():
    with patch(
        "devdoctor.checks.tools.shutil.which",
        return_value=None,
    ):
        result = check_git()

    assert result.status == Status.MISSING


def test_git_timeout():
    with (
        patch(
            "devdoctor.checks.tools.shutil.which",
            return_value="/usr/bin/git",
        ),
        patch(
            "devdoctor.checks.tools.subprocess.run",
            side_effect=subprocess.TimeoutExpired(
                cmd=["git", "--version"],
                timeout=5,
            ),
        ),
    ):
        result = check_git()

    assert result.status == Status.ERROR
