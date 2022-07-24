from tkinter.font import Font
from typing import Any, Callable, TypeAlias

from .screen import Screen


_FontDescription: TypeAlias = (
    str  # "Helvetica 12"
    | Font  # A font object constructed in Python
    | list[Any]  # ("Helvetica", 12, BOLD)
    | tuple[Any, ...]
)


class Button:
    def __init__(self, text: str, width: int, 
        height: int, bg: str = "#fff", fg: str = "#000", font: _FontDescription = ...,
        border: str = "#000", border_width: int = 1, callback: Callable = None) -> None:
        self.text = text

        self.width = width
        self.height = height

        self._bg = bg
        self._fg = fg
        self._font = font

        self._border = border
        self._border_width = border_width

        self.callback = callback or (lambda: 1)

    def place(self, screen: Screen, x: int, y: int):
        screen.canv.create_rectangle(
            x, y, x+self.width, y+self.height, fill=self._bg, 
            outline=self._border, width=self._border_width, tags="CustomButton"
        )
        screen.canv.create_text(
            x + (self.width//2), y + (self.height//2) - 2, text=self.text, 
            fill=self._fg, font=self._font, tags="CustomButtonText"
        )
        screen.buttons.append((self, x, y))
