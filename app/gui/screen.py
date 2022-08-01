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
    BUTTON_TAGS = ["CustomButton", "CustomButtonText"]

    def __init__(self, canvas: tkinter.Canvas) -> None:
        self.canv = canvas
        self.buttons: list[tuple[Button, int, int]] = []

        # Mouse button press events
        [canvas.tag_bind(tag, "<ButtonPress>", lambda e: self._on_mouse_click(
            MouseEvent(e.x, e.y, e.num, True)
        )) for tag in self.BUTTON_TAGS]

        # Mouse button release events
        [canvas.tag_bind(tag, "<ButtonRelease>", lambda e: self._on_mouse_click(
            MouseEvent(e.x, e.y, e.num, False)
        )) for tag in self.BUTTON_TAGS]

    def _on_mouse_click(self, event: MouseEvent):
        """
        Base method that is called when the user clicks on the screen.
        Fires the on_mouse_click method if this screen has it.
        Fires button callback if it was clicked.
        
        :param event:MouseEvent: Mouse button click event
        """
        if hasattr(self, "on_mouse_click"):
            self.on_mouse_click(event)

        for btn, x, y in self.buttons:
            if (x <= event.x <= x + btn.width) and \
                    (y <= event.y <= y + btn.height):
                # noinspection PyProtectedMember
                btn._on_mouse_click(event)

    def event(self, func: Callable):
        """
        Decorator that registers an event handler.
        
        :param func:Callable: Specify the function that is called when the event occurs
        """
        if callable(func):
            setattr(self, func.__name__, func)
