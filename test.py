import os

from app.controllers.launcher import get_current_launch_data, launch_java
from app.controllers.extractor import extract_data

from app.core.errors import ModpackDoesNotExists

os.system("cls")


get_option = input("1 - Запуск кабума\n2 - Обновить дату\n>>> ")

if get_option == "1":
    try:
        modpack = input("Введите модпак\n>>> ")
        launch_java(get_current_launch_data("1.7.10", modpack))
    except ModpackDoesNotExists:
        print("Не ну ты реально конч?")
elif get_option == "2":
    extract_data(True)
else:
    print("Ты даун?")

