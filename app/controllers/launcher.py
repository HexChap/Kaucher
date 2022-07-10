import os
import re
import json
from pathlib import Path

import psutil

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
                  "--assetIndex {ver} --uuid {uuid} --accessToken {token} "
                  "--version {ver} --username {username} --userProperties {{}} "
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


def get_launch_data():
    with open("data") as f:
        return launch_data.LaunchData(**json.load(f))


def launch_java(data: launch_data.LaunchData, ver: str, modpack: str):
    if ver not in modpacks.keys():
        raise errors.WrongVersionError

    if modpack not in modpacks[ver]:
        raise errors.ModpackDoesNotExists

    os.chdir(data.kaboom_dir / "modpacks" / ver / "modpacks" / modpack)

    os.popen(
        launch_cmdline.format(
            java_path=data.kaboom_dir / "runtime-windows-x64" / "bin" / "javaw.exe",
            memory=data.memory,
            natives=data.kaboom_dir / "modpacks" / ver / "natives",
            cp_libs=data.kaboom_dir / "modpacks" / ver / "libs" / "*",
            tweak_class = tweak_classes[ver],
            game_dir=data.kaboom_dir / "modpacks" / ver / "modpacks" / modpack,
            assets=data.kaboom_dir / "modpacks" / ver / "assets",
            ver=ver,
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


def remove_nguard(data: launch_data.LaunchData):
    """
    Removes nGuardMod.

    :param data: Launch data
    :return:
    """

    game_dir = data.kaboom_dir / "modpacks" / "1.7.10" / "tesla"

    n_guard_path = game_dir / "mods" / "1.7.10" / "nGuardMod.jar"
    if os.path.isfile(n_guard_path):
        os.remove(n_guard_path)
