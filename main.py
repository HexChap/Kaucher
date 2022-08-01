from dataclasses import dataclass
import os
from tkinter import Button, Canvas, Tk
import tkinter

from app.controllers import launcher, extractor
from app import gui


class Utils:
    @staticmethod
    def screen_size(tk_: Tk) -> list[int]:
        """
        Returns the width and height of the user's screen in pixels.

        :return: list[int] Screen width and height as list
        """
        return [tk_.winfo_screenwidth(), tk_.winfo_screenheight()]


@dataclass
class Theme:
    bg: str
    outline: str
    mp_bg: str
    fg: str
    font_family: tuple


class App:
    def __init__(self) -> None:
        self._window_title = "Kaucher"
        self._window_size = [650, 450]

        self.theme = Theme(
            bg="#161620",
            outline="#1f2029",
            mp_bg="#1a1b26",
            fg="#cccccc",
            font_family=("Arial", 13)
        )

        self._root = Tk(self._window_title, self._window_title)

        self.init_window()

        self._canv = Canvas(
            self._root, bg=self.theme.bg, width=self._window_size[0], 
            height=self._window_size[1], highlightthickness=0
        )
        self._canv.pack()

    def init_window(self):
        self._root.title(self._window_title)

        ss = Utils.screen_size(self._root)
        self._root.geometry(
            f"{self._window_size[0]}x{self._window_size[1]}"
            f"+{ss[0] // 2 - self._window_size[0] // 2}"
            f"+{ss[1] // 2 - self._window_size[1] // 2}"
        )

        self._root.resizable(False, False)

    def clear_screen(self):
        self._canv.delete("all")

    # Menus
    def show_mp_startup_page(self, page: int = 1):
        """
        Displays all modpacks.        
        
        :param page:int=1: Determine which page of modpacks to display
        """
        self.clear_screen()

        MP_FOR_PAGE = 6
        mp_list = []

        for k, v in launcher.modpacks.items():
            mp_list.extend([[mp, k] for mp in v])

        screen = gui.Screen(self._canv)

        # Add buttons with mp names
        for i, mp in enumerate(mp_list[(page-1)*MP_FOR_PAGE:page*MP_FOR_PAGE]):
            self._canv.create_rectangle(
                75 + ((i - 3 * (i > 2)) * 187.5), 60 + 190 * (i > 2),
                75 + ((i - 3 * (i > 2)) * 187.5) + 125, 200 + 190 * (i > 2),
                fill=self.theme.mp_bg, outline=self.theme.outline, width=1.5
            )

            # Create modpack info text
            self._canv.create_text(
                137.5 + ((i - 3 * (i > 2)) * 187.5), 80 + 190 * (i > 2),
                text=mp[0].title(), font=self.theme.font_family,
                fill=self.theme.fg, justify="center"
            )
            self._canv.create_text(
                137.5 + ((i - 3 * (i > 2)) * 187.5), 100 + 190 * (i > 2),
                text=mp[1], font=self.theme.font_family,
                fill=self.theme.fg, justify="center"
            )

            # Create buttons
            x, y = 137.5 + 187.5 * ((i - 3 * (i > 2))), 190 * (i > 2)

            # Create Modpack start button
            # TODO: Callback (launch mp)
            gui.Button(
                text="Запустить",
                width=90,
                height=30,
                bg=self.theme.bg,
                fg=self.theme.fg,
                font=("Arial", 13),
                border=self.theme.outline,
                border_width=1.5,
                callback=lambda mp=mp: launcher.launch_java(
                    launcher.get_mp_launch_data(mp[1], mp[0])
                )
            ).place(screen, x-45, y+185-15)

            # Create Modpack open folder button
            gui.Button(
                text="📁",
                width=34,
                height=30,
                bg=self.theme.bg,
                fg=self.theme.fg,
                font=("Arial", 15),
                border=self.theme.outline,
                border_width=1.5,
                callback=lambda mp=mp: os.startfile(launcher.\
                    get_mp_launch_data(mp[1], mp[0]).mp_dir)
            ).place(screen, x-17, y+140-15)

    def run(self):
        self._root.after(1000, self.show_mp_startup_page)
        self._root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
