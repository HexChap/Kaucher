import os
import psutil
import time

from pymenu import *
from pymenu import colorpy
from threading import Thread


def show_mp_select_menu(prev_menu: Menu):
    columns = ["Сервер", "Версия"]
    modpacks = {
        "1.7.10": ["Tesla", "SkyFactory"]
    }

    menu = ColumnsMenu(
        "Выберите сборку для запуска",
        columns, exit_option=ExitOption("Назад", lambda: prev_menu.start())
    )

    def callback(o: OptionRow):
        # TODO: Start modpack

        modpack_menu = Menu(
            f"Сборка {o.modpack_name} была запущена!",
            exit_option=ExitOption("Назад", lambda: menu.start())
        )

        modpack_menu.start()

    for sv in modpacks.keys():
        menu.add_rows([
            OptionRow(columns, [sn, sv], callback, modpack_name=sn)
            for sn in modpacks.get(sv)
        ])

    menu.start()


def show_account_update_menu(prev_menu: Menu):
    menu = Menu(
        "Запустите любую сборку из официального лаунчера Kaboom 2.0",
        exit_option=ExitOption("Назад", lambda: prev_menu.start())
    )

    def update_account():
        while menu.is_active:
            for proc in psutil.process_iter():
                if proc.name() == "javaw.exe":
                    cmd_line = proc.cmdline()

                    # if "accessToken" not in cmd_line:
                    #     continue

                    proc.kill()

                    menu.title = "Выберите аккаунт"
                    menu.add_option(Option(
                        cmd_line[cmd_line.index("--username")+1]
                    ))

                    return

            time.sleep(0.5)

    Thread(target=update_account).start()

    menu.start()


def main():
    main_menu = Menu(
        "Выберите действие",
        exit_option=ExitOption("Выйти", lambda: [colorpy.cls(), os.exit(0)])
    )

    main_menu.add_options([
        Option("Запустить сборку", lambda: show_mp_select_menu(main_menu)),
        Option("Обновить данные", lambda: show_account_update_menu(main_menu))
    ])

    while True:
        main_menu.start()


if __name__ == "__main__":
    main()
