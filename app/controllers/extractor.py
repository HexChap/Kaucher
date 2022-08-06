import json
from pathlib import Path
import psutil

from app.schemas import launch_data_schemas


def extract_data() -> launch_data_schemas.LaunchData:
    """
    Finds javaw process and extracts info from its start command line.

    :return: Username, game directory, access token and uuid
    """
    for proc in psutil.process_iter():
        if proc.name() == "javaw.exe":
            j_cmdline = proc.cmdline()

            if "--accessToken" not in j_cmdline:
                continue

            data = launch_data_schemas.LaunchData(
                username=_get_value_cmdline("--username", j_cmdline),
                kaboom_dir=Path(_get_value_cmdline("--assetsDir", j_cmdline)).parent.parent.parent,
                memory="2048",
                uuid=_get_value_cmdline("--uuid", j_cmdline),
                access_token=_get_value_cmdline("--accessToken", j_cmdline)
            )

            return update_data_file(data)


def get_static_data() -> launch_data_schemas.LaunchData:
    with open("data") as f:
        static_data = launch_data_schemas.LaunchData(**json.load(f))

    return static_data


def get_mp_launch_data(version: str, mp_name: str) -> launch_data_schemas.ModpackLaunchData:
    """
    Returns a ModpackLaunchData object from modpack version and modpack name.

    :param version:str: Version of the modpack.
    :param mp_name:str: Name of the modpack.
    :return: ModpackLaunchData.
    """
    static_data = get_static_data()

    return launch_data_schemas.ModpackLaunchData(
        **static_data.dict(),
        mp_dir=static_data.kaboom_dir / "modpacks" / version / "modpacks" / mp_name,
        version=version,
        modpack=mp_name
    )


def update_data_file(new_data: launch_data_schemas.LaunchData) -> launch_data_schemas.LaunchData:
    """
    Updates data file with new values.

    :param new_data: Launch data
    :return: app.schemas.launch_data.LaunchData
    """
    with open("data", "w+") as f:
        f.write(new_data.json())

    return new_data


def _get_value_cmdline(arg: str, data: list):
    """
    Extract value by arg from *psutil.Process.cmdline* like list.

    :param arg: some arg string
    :param data: cmdline list
    :return:
    """
    return data[data.index(arg) + 1]
