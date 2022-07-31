import os

from pymenu import *
from pymenu import colorpy


# noinspection PyProtectedMember,PyTypeChecker
def main():
    columns = ["Сервер", "Версия"]
    servers = {
        "1.7.10": ["Tesla", "SkyFactory"]
    }

    server_select_menu = ColumnsMenu(
        "Выберите сборку для запуска",
        columns, exit_option=ExitOption("Выйти", lambda: [colorpy.cls(), os._exit(0)])
    )

    # noinspection PyTypeChecker
    def callback(o: OptionRow):
        # TODO: Start server

        server_menu = Menu(
            f"Сборка {o.server_name} была запущена!",
            exit_option=ExitOption("Назад", lambda: server_select_menu.start())
        )

        server_menu.start()

    for sv in servers.keys():
        server_select_menu.add_rows([
            OptionRow(columns, [sn, sv], callback, server_name=sn)
            for sn in servers.get(sv)
        ])

    while True:
        server_select_menu.start()


if __name__ == "__main__":
    main()
