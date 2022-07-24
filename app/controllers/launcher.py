import os
import re
import json

from app.schemas import launch_data

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


def get_mp_launch_data(version: str, mp_name: str):
    """
    Returns a ModpackLaunchData object from modpack version and modpack name.
    
    :param version:str: Version of the modpack.
    :param modpack:str: Name of the modpack.
    :return: ModpackLaunchData.
    """
    with open("data") as f:
        static_data = launch_data.LaunchData(**json.load(f))

    return launch_data.ModpackLaunchData(
        **static_data.dict(),
        mp_dir=static_data.kaboom_dir / "modpacks" / version / "modpacks" / mp_name,
        version=version,
        modpack=mp_name
    )


def launch_java(data: launch_data.ModpackLaunchData, use_kaboom_java: bool = True):
    """
    Launches a Minecraft process with given modpack data.
    
    :param data:launch_data.ModpackLaunchData: Modpack launch data.
    :param use_kaboom_java:bool=True: Determine whether or not to use the Kaboom java runtime.
    """
    version_dir = data.kaboom_dir / "modpacks" / data.version
    java_path = (data.kaboom_dir / "runtime-windows-x64" / "bin" / "javaw.exe") if use_kaboom_java else "javaw.exe"

    os.chdir(data.mp_dir)

    os.popen(
        launch_cmdline.format(
            java_path=java_path,
            memory=data.memory,
            natives=version_dir / "natives",
            cp_libs=version_dir / "libs" / "*",
            tweak_class = tweak_classes[data.version],
            game_dir=version_dir / "modpacks" / data.modpack,
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
