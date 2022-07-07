import os
import sys

import colorama

colorama.init()


if os.name == "nt":
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [
            ("size", ctypes.c_int),
            ("visible", ctypes.c_byte)
        ]


colors = {
    "0": "black",
    "1": "blue",
    "2": "green",
    "3": "cyan",
    "4": "red",
    "5": "magenta",
    "6": "yellow",
    "7": "lightgrey",
    "8": "grey",
    "9": "lightblue",
    "a": "lightgreen",
    "b": "lightcyan",
    "c": "lightred",
    "d": "lightmagenta",
    "e": "lightyellow",
    "f": "white"
}
styles = {
    "b": "bright",
    "d": "dim",
    "n": "normal",
    "r": "reset all",
}


def colored(string: str) -> str:
    """
    Uses colorama to colorify given string.\n
    Works like Minecraft chat coloring:\n
    \t\"&cHello\" = \"Hello\" string with light red symbols.\n
    \t\"$cHello\" = \"Hello\" string with light red background.\n
    \t\"$7&0Hello\" = \"Hello\" string with light grey background and black symbols.\n
    """

    colorama.reinit()

    colors_dict = {
        "0": "BLACK",
        "1": "BLUE",
        "2": "GREEN",
        "3": "CYAN",
        "4": "RED",
        "5": "MAGENTA",
        "6": "YELLOW",
        "7": "WHITE",
        "8": "LIGHTBLACK_EX",
        "9": "LIGHTBLUE_EX",
        "a": "LIGHTGREEN_EX",
        "b": "LIGHTCYAN_EX",
        "c": "LIGHTRED_EX",
        "d": "LIGHTMAGENTA_EX",
        "e": "LIGHTYELLOW_EX",
        "f": "LIGHTWHITE_EX"
    }
    styles_dict = {
        "b": "BRIGHT",
        "d": "DIM",
        "n": "NORMAL",
        "r": "RESET_ALL"
    }

    out = ""
    i = 0
    
    while True:
        if string[i] in ["#", "$", "&"] and i == len(string)-2:
            i += 1

        elif string[i] == "#" and string[i+1] in styles_dict:
            out += getattr(colorama.Style, styles_dict[string[i+1]])
            i += 1

        elif string[i] == "$" and string[i+1] in colors_dict:
            out += getattr(colorama.Back, colors_dict[string[i+1]])
            i += 1

        elif string[i] == "&" and string[i+1] in colors_dict:
            out += getattr(colorama.Fore, colors_dict[string[i+1]])
            i += 1

        else:
            out += string[i]

        i += 1

        if i == len(string):
            out += colorama.Style.RESET_ALL
            break

    return out


def cls():
    """
    Another way to clear the console.
    """
    print("\x1b[2J", end="")


def hide_cursor():
    """
    Hides the console cursor.
    """
    if os.name == "nt":
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        
    elif os.name == "posix":
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


def show_cursor():
    """
    Shows the console cursor.
    """
    if os.name == "nt":
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        
    elif os.name == "posix":
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
