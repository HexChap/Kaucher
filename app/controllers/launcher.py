import os
import re
import json
import shutil
from pathlib import Path

from app.schemas import launch_data
from app.core import errors

GAME_DIR_PATTERN = re.compile(r"--gameDir (\S+)")
RPC_CONFIG = """
# Configuration file

general {
    # Servername [default: Kaboom 2.0]
    S:Servername=%s
}
"""
launch_cmdline = ("\"{java_path}\" "
                  "-Xmx{memory}m -Dfml.ignoreInvalidMinecraftCertificates=true "
                  "\"-Djava.library.path={natives}\" "
                  "-cp \"{cp_libs}\" net.minecraft.launchwrapper.Launch "
                  "--tweakClass {tweak_class}.fml.common.launcher.FMLTweaker "
                  "--gameDir \"{game_dir}\" --assetsDir \"{assets}\" "
                  "--assetIndex {version} --uuid {uuid} --accessToken {token} "
                  "--version {version} --username {username} --userProperties {{}} "
                  "--userType mojang")
tweak_classes = {
    "1.7.10": "cpw.mods",
    "1.12.2": "net.minecraftforge"
}
modpacks = {
        "1.7.10": [
            "tesla",
            "skyfactory",
            "spacex",
            "nevermine",
            "dragonglory",
            "darkshire"
        ],
        "1.12.2": [
            "edison",
            "pixelmon",
            "terrafirmacraft",
            "nightmare",
            "cybermagic",
            "claustrophobia"
        ]
    }


def get_current_launch_data(version: str, modpack: str):
    if version not in modpacks.keys():
        raise errors.WrongVersionError

    if modpack not in modpacks[version]:
        raise errors.ModpackDoesNotExists

    with open("data") as f:
        static_data = launch_data.LaunchData(**json.load(f))

    return launch_data.CurrentLaunchData(
        version=version,
        modpack=modpack,
        **static_data.dict()
    )


def launch_java(data: launch_data.CurrentLaunchData):
    version_dir = data.kaboom_dir / "modpacks" / data.version
    modpack_dir = version_dir / "modpacks" / data.modpack

    remove_nguard(data)
    extend_mods(data)

    os.chdir(modpack_dir)

    os.popen(
        launch_cmdline.format(
            java_path=data.kaboom_dir / "runtime-windows-x64" / "bin" / "javaw.exe",
            memory=data.memory,
            natives=version_dir / "natives",
            cp_libs=version_dir / "libs" / "*",
            tweak_class = tweak_classes[data.version],
            game_dir=modpack_dir,
            assets=version_dir / "assets",
            version=data.version,
            uuid=data.uuid,
            token=data.access_token,
            username=data.username,
        )
    )


def modify_rpc(data: launch_data.LaunchData, server: str | int):
    """
    Modifiying Discord RPC.

    :param data: Launch data
    :param server: What will be written in the **Servername** field
    :return: None
    """
    if not isinstance(data, launch_data.LaunchData):
        raise TypeError

    game_dir = data.kaboom_dir / "modpacks" / "1.7.10" / "tesla"

    with open(game_dir / "config" / "RPC.cfg", mode="w+") as f:
        f.write(RPC_CONFIG % server)


def remove_nguard(data: launch_data.CurrentLaunchData):
    """
    Removes nGuardMod.

    :param data: Launch data
    :return:
    """
    modpacks_dir = data.kaboom_dir / "modpacks" / data.version / "modpacks" / data.modpack
    n_guard_path = modpacks_dir / "mods" / "1.7.10" / "nGuardMod.jar"

    if os.path.isfile(n_guard_path):
        os.remove(n_guard_path)


def extend_mods(data: launch_data.CurrentLaunchData):
    """
    Extends mods in the modpack dir via mods from the **mods** folder.

    :param data: Launch data
    :return:
    """
    local_mods_folder = Path(r"mods")
    modpacks_dir = data.kaboom_dir / "modpacks" / data.version / "modpacks" / data.modpack

    for file in os.listdir(local_mods_folder):
        print(f"+ Extended with {file}")
        if os.path.exists(modpacks_dir / "mods" / file):
            continue

        shutil.copy(local_mods_folder / file, modpacks_dir / "mods")
