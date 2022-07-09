import psutil

from app.controllers.launcher import launch_java, get_lauch_data
from app.controllers.extractor import extract_data


psutil.Process(list(filter(lambda proc: proc.name() == "javaw.exe", psutil.process_iter()))[0].pid).kill()
