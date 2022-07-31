from tkinter.font import Font
from typing import Any, Callable, TypeAlias

from .screen import MouseEvent, Screen

_FontDescription: TypeAlias = (
        str  # "Helvetica 12"
        | Font  # A font object constructed in Python
        | list[Any]  # ("Helvetica", 12, BOLD)
        | tuple[Any, ...]
)


class Button:
    def __init__(
        self, text: str, width: int,
        height: int, bg: str = "#fff", fg: str = "#000", font: _FontDescription = ...,
        border: str = "#000", border_width: int = 1, callback: Callable = None
    ) -> None:
        self.text = text

        self.width = width
        self.height = height

        # Appearance
        self._bg = bg
        self._fg = fg
        self._font = font

        self._border = border
        self._border_width = border_width

        # Functionality
        self._screen = None
        self.callback = callback or (lambda: 1)

        # Canvas parts
        self._c_bg: int = 0
        self._c_text: int = 0

    def on_mouse_click(self, event: MouseEvent):
        if event.button == 1:
            if event.state:
                self._screen.canv.itemconfig(self._c_bg, fill="#333349")

            else:
                self._screen.canv.itemconfig(self._c_bg, fill=self._bg)
                self.callback()

    def place(self, screen: Screen, x: int, y: int):
        """
        Places the button on the specified screen.
        
        :param screen:Screen: Screen object.
        :param x:int: x-coordinate of the button.
        :param y:int: y-coordinate of the button.
        """
        self._screen = screen

        self._c_bg = screen.canv.create_rectangle(
            x, y, x + self.width, y + self.height, fill=self._bg,
            outline=self._border, width=self._border_width, tags="CustomButton"
        )
        self._c_text = screen.canv.create_text(
            x + (self.width // 2), y + (self.height // 2) - 2, text=self.text,
            fill=self._fg, font=self._font, tags="CustomButtonText"
        )

        screen.buttons.append((self, x, y))
