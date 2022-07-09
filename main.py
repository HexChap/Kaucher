import os

import psutil

from app.controllers.launcher import launch_java, get_lauch_data
from app.controllers.extractor import extract_data

# extract_data()
launch_java(get_lauch_data(), "1.7.10", "tesla")
# os.chdir("D:\\Games\\Kaboom\\modpacks\\1.7.10\\modpacks\\tesla")
# cmd = (
#             fr"D:\Games\Kaboom\runtime-windows-x64\bin\javaw.exe "
#             f"-Xmx2048m -Dfml.ignoreInvalidMinecraftCertificates=true "
#             f"\"-Djava.library.path=D:\\Games\\Kaboom\\modpacks\\1.7.10\\natives\" "
#             f"-cp \"D:\\Games\\Kaboom\\modpacks\\1.7.10\\libs\\*\" net.minecraft.launchwrapper.Launch "
#             f"--tweakClass cpw.mods.fml.common.launcher.FMLTweaker "
#             f"--gameDir \"D:\\Games\\Kaboom\\modpacks\\1.7.10\\modpacks\\tesla\" --assetsDir \"D:\\Games\\Kaboom\\modpacks\\1.7.10\\assets\" "
#             f"--assetIndex 1.7.10 --uuid c82f0908-8624-3a53-9817-beaa64daf5b5 --accessToken 0a3d4d60-2d59-483d-b4ba-c07f3a95b1b3 "
#             f"--version 1.7.10 --username Specialized_ --userProperties {{}} "
#             "--userType mojang"
#         )
# os.popen(cmd)
# input()
# psutil.Process(list(filter(lambda proc: proc.name() == "javaw.exe", psutil.process_iter()))[0].pid).kill()
