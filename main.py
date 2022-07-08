import psutil

from app.controllers.launcher import extract_data, modify_rpc


modify_rpc(extract_data(), 2)

psutil.Process(list(filter(lambda proc: proc.name() == "javaw.exe", psutil.process_iter()))[0].pid).kill()
