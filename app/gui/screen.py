import tkinter

from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .button import Button


@dataclass
class MouseEvent:
    x: int
    y: int
    button: int
    state: bool

    def __str__(self) -> str:
        return f"<MouseEvent x={self.x}, y={self.y}, button={self.button}, state={self.state}>"

    def __repr__(self) -> str:
        return self.__str__()


class Screen:
    def __init__(self, canvas: tkinter.Canvas) -> None:
        self.canv = canvas
        self.buttons: list[tuple[Button, int]] = []

        BUTTON_TAGS = ["CustomButton", "CustomButtonText"]

        # Mouse button press events
        [canvas.tag_bind(tag, "<ButtonPress>", lambda e: self._on_mouse_click(
            MouseEvent(e.x, e.y, e.num, True)
        )) for tag in BUTTON_TAGS]

        # Mouse button release events
        [canvas.tag_bind(tag, "<ButtonRelease>", lambda e: self._on_mouse_click(
            MouseEvent(e.x, e.y, e.num, False)
        )) for tag in BUTTON_TAGS]

    def _on_mouse_click(self, event: MouseEvent):
        if hasattr(self, "on_mouse_click"):
            self._on_mouse_click(event)

        for b, x, y in self.buttons:
            if (event.x >= x and event.x <= x+b.width) and (event.y >= y and event.y <= y+b.height):
                b.callback()

    def event(self, func: Callable):
        if callable(func):
            setattr(self, func.__name__, func)
