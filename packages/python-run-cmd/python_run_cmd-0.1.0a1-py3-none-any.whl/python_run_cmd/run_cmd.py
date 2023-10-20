"""Run a command."""
import subprocess as sp

import rich
from loguru import logger


def run_cmd(cmd, mute_stdout=True, mute_stderr=False):
    """
    Execute cmd.

    Args:
    ----
        cmd: command to execute
        mute_stdout: default True, do not output stdout if True
        mute_stderr: default False, do not output stderr if True

    Returns:
    -------
        CompletedProcess(args=cmd, returncode=0|..., stdout='...', stderr='...'
    """
    logger.info(f"{cmd=}")
    ret = sp.run(cmd, capture_output=True, check=False, shell=True, encoding="utf8")
    if ret.stdout and not mute_stdout:
        rich.print(ret.stdout)
    if ret.stderr and not mute_stderr:
        rich.print("[red bold]" + ret.stderr)

    return ret
