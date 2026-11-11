import subprocess
from unittest.mock import patch

from devdoctor.checks.tools import check_git
from devdoctor.models import Status


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
