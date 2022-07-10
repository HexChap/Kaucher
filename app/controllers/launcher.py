import os.path
import re
from pathlib import Path

import psutil

from app.schemas import launch_data

GAME_DIR_PATTERN = re.compile(r"--gameDir (\S+)")
RPC_CONFIG = """
# Configuration file

general {
    # Servername [default: Kaboom 2.0]
    S:Servername=%s
}
"""


def extract_data() -> launch_data.LaunchData:
    """
    Finds javaw process and extracts info from its start command line.

    :return: Username, game directory, access token and uuid
    """

    while True:
        for proc in psutil.process_iter():
            if proc.name() == "javaw.exe":
                j_cmdline = proc.cmdline()

                if "--accessToken" not in j_cmdline:
                    continue

                return launch_data.LaunchData(
                    username=_get_value_cmdline("--username", j_cmdline),
                    game_dir=Path(_get_value_cmdline("--gameDir", j_cmdline)),
                    uuid=_get_value_cmdline("--uuid", j_cmdline),
                    access_token=_get_value_cmdline("--accessToken", j_cmdline)
                )


def modify_rpc(data: launch_data.LaunchData, server: str | int):
    """
    Modifiying Discord RPC.

    :param data: Launch data
    :param server: What will be written in the **Servername** field
    :return: None
    """
    if not isinstance(data, launch_data.LaunchData) or not isinstance(server, str):
        raise TypeError

    with open(data.game_dir / "config" / "RPC.cfg", mode="w+") as f:
        f.write(RPC_CONFIG % server)


def remove_nguard(launch_data: launch_data.LaunchData):
    """
    Removes nGuardMod.

    :param launch_data: Launch data
    :return:
    """

    n_guard_path = launch_data.game_dir / "mods" / "1.7.10" / "nGuardMod.jar"
    if os.path.isfile(n_guard_path):
        os.remove(n_guard_path)


def _get_value_cmdline(arg: str, data: list):
    """
    Extract value by arg from *psutil.Process.cmdline* like list.

    :param arg: some arg string
    :param data: cmdline list
    :return:
    """
    return data[data.index(arg) + 1]
