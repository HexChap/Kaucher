import psutil
import os

from win32process import GetWindowThreadProcessId
from types import FunctionType, LambdaType
from win32gui import GetForegroundWindow
from typing import List, Union, Any
from pynput import keyboard

from pymenu import colorpy


def get_longest(_list: list, key: LambdaType = lambda i: len(i)) -> str:
    return sorted([str(s) for s in _list], key=key, reverse=True)[0]


class Option:
    def __init__(self, name: str, callback: Union[FunctionType, LambdaType] = None, **data) -> None:
        self.name = name
        self.callback = callback
        self.is_selected = False

        [setattr(self, n, v) for n, v in data.items()]


class OptionRow:
    def __init__(self, columns: List[str], row: Union[list, dict],
                 callback: Union[FunctionType, LambdaType] = None, **data) -> None:
        self.columns = columns
        self.callback = callback
        self.is_selected = False

        if isinstance(row, list):
            if len(columns) < len(row):
                raise ValueError(f"Incorrect len of provided 'row' attr: \
                    {len(row)} (columns len: {len(columns)}).")

            self.row = row + [None] * (len(columns) - len(row))

        elif isinstance(row, dict):
            self.row = [row[i] if i in row else None for i in self.columns]

        else:
            raise ValueError(f"Incorrect type of provided value ({row}) for 'row' attr: {type(row)}.")

        [setattr(self, n, v) for n, v in data.items()]


class ExitOption(Option):
    pass


class Menu:
    def __init__(self, title: str = None, options: List[Option] = None,
                 selected_option: int = 0, exit_option: ExitOption = None) -> None:
        self.title = title

        self.options: List[Option] = [o for o in options
                                      if isinstance(o, Option)] if options else []

        self.exit_option = exit_option
        self.selected_option = selected_option

    def add_option(self, option: Option) -> None:
        self.options.append(option)

    def add_options(self, options: List[Option]) -> None:
        self.options.extend(options)

    def __render(self) -> None:
        """ Custom render method should return\n
        Tuple: (longest: List[int], rendered: List[str]).
        """
        buffer = ["\x1b[2J"]
        longest = self.get_longest_option()

        if hasattr(self, "render"):
            custom_render = self.render(self)
            longest = custom_render[0]

            buffer.extend([f"| {i}" for i in custom_render[1]])

        else:
            for o in self.options:
                line_start = f"| • #r$f&0|#r " if o.is_selected else f"|   | "

                if isinstance(o, ExitOption):
                    if len(self.options) > 1:
                        buffer.append(f"|   |{' ' * (longest + 4)}|")

                buffer.append(colorpy.colored(line_start +
                                              f"{o.name}#r{' ' * (longest - len(o.name) + 3)}|"))

        if self.title:
            buffer[1:0] = [
                "_" * (longest + 10), f"|{' ' * (longest + 8)}|",
                f"|{self.title.center(longest + 8)}|", f"|{'_' * (longest + 8)}|",
                f"|{' ' * (longest + 8)}|"
            ]

        else:
            buffer[1:0] = [f"{'_' * (longest + 10)}", f"|{' ' * (longest + 8)}|"]

        buffer.append(f"|{' ' * (longest + 8)}|")
        buffer.append("‾" * (longest + 10))

        print("\n".join(buffer))

    def __on_key_press(self, key) -> Union[None, bool]:
        fgw_pid = GetWindowThreadProcessId(GetForegroundWindow())[1]

        if not os.getpid() in [p.pid for p in psutil.Process(fgw_pid).children(recursive=True)]:
            return

        key = key._name_ if "_name_" in key.__dict__ else None

        if key is None or key not in ["enter", "up", "down"]:
            return

        if key == "enter":
            return False

        self.options[self.selected_option].is_selected = False

        if key == "up":
            self.selected_option -= 1

            if self.selected_option == -1:
                self.selected_option = len(self.options) - 1

        elif key == "down":
            self.selected_option += 1

            if self.selected_option > len(self.options) - 1:
                self.selected_option = 0

        self.options[self.selected_option].is_selected = True
        self.__render()

    def event(self, func) -> None:
        if isinstance(func, FunctionType):
            setattr(self, func.__name__, func)

    def start(self) -> Union[None, Option]:
        if self.exit_option:
            if len(self.options) > 0 and not isinstance(self.options[-1], ExitOption):
                self.options.append(self.exit_option)

            elif len(self.options) == 0:
                self.options.append(self.exit_option)

        self.options[self.selected_option].is_selected = True

        colorpy.hide_cursor()
        self.__render()

        with keyboard.Listener(on_press=self.__on_key_press) as listener:
            listener.join()

        os.system("cls")
        colorpy.show_cursor()

        o = self.options[self.selected_option]

        if o.callback is not None:
            if o.callback.__code__.co_argcount > 0:
                o.callback(o)

            else:
                o.callback()

        else:
            return o

    def get_longest_option(self) -> int:
        return len(get_longest([self.title,
                                *[o.name for o in self.options]], lambda i: len(i)))


class ColumnsMenu:
    def __init__(self, title: str = None, columns: List[str] = None,
                 rows: List[OptionRow] = None, selected_row: int = 0,
                 exit_option: ExitOption = None) -> None:
        self.title = title

        self.columns = columns or []
        self.rows: List[OptionRow] = [r for r in rows
                                      if isinstance(r, OptionRow)] if rows else []

        self.exit_option = exit_option
        self.selected_row = selected_row

    def add_row(self, row: OptionRow) -> None:
        self.rows.append(row)

    def add_rows(self, rows: List[OptionRow]) -> None:
        self.rows.extend(rows)

    def __render(self) -> None:
        """ Custom render method should return\n
        Tuple: (longest: List[int], rendered: List[str]).
        """
        buffer = ["\x1b[2J"]
        longest = self.get_longest_option()

        row_len = sum(longest) + len(self.columns) * 3
        empty_row = f"|   |{'|'.join([' ' * (i + 2) for i in longest])}|"

        if hasattr(self, "render"):
            custom_render = self.render(self)
            longest = custom_render[0]
            buffer.extend([f"| {i}" for i in custom_render[1]])

        else:
            for r in self.rows:
                if isinstance(r, ExitOption):
                    v = r.name

                    s = (f"{empty_row}\n" if len(self.rows) > 1 else "") + \
                        (f"| • | {v}" if r.is_selected else f"|   | {v}") + \
                        " " * (longest[0] - len(v)) + " |"

                    if len(longest) > 1:
                        s += "".join([f"{' ' * (i + 2)}|" for i in longest[1:]])

                else:
                    s = " ".join([f"{v}{' ' * (longest[i] - len(v))} |"
                                  for i, v in enumerate(r.row)])

                    s = f"| • | {s}" if r.is_selected else f"|   | {s}"

                buffer.append(s)

        if self.title:
            buffer[1:0] = [
                "_" * (row_len + 5), f"|{' ' * (row_len + 3)}|",
                f"|{self.title.center(row_len + 3)}|", f"|{'_' * (row_len + 3)}|",
                empty_row,
                f"|   |{'|'.join([c.center(longest[i] + 2) for i, c in enumerate(self.columns)])}|",
                empty_row
            ]

        else:
            buffer[1:0] = [
                "_" * (sum(longest) + 7), empty_row,
                f"|   |{'|'.join([c.center(longest[i] + 2) for i, c in enumerate(self.columns)])}|",
                f"|___|{'|'.join(['_' * (i + 2) for i in longest])}|",
                empty_row
            ]

        buffer.append(f"|   |{'|'.join([' ' * (i + 2) for i in longest])}|")
        buffer.append("‾" * (sum(longest) + len(self.columns) * 3 + 5))

        print("\n".join(buffer))

    def __on_key_press(self, key) -> Union[None, bool]:
        fgw_pid = GetWindowThreadProcessId(GetForegroundWindow())[1]

        if not os.getpid() in [p.pid for p in psutil.Process(fgw_pid).children(recursive=True)]:
            return

        key = key._name_ if "_name_" in key.__dict__ else None

        if key is None or key not in ["enter", "up", "down"]:
            return

        if key == "enter":
            return False

        self.rows[self.selected_row].is_selected = False

        if key == "up":
            self.selected_row -= 1

            if self.selected_row == -1:
                self.selected_row = len(self.rows) - 1

        elif key == "down":
            self.selected_row += 1

            if self.selected_row > len(self.rows) - 1:
                self.selected_row = 0

        self.rows[self.selected_row].is_selected = True
        self.__render()

    def event(self, func) -> None:
        if isinstance(func, FunctionType):
            setattr(self, func.__name__, func)

    def start(self) -> Union[None, OptionRow]:
        if self.exit_option:
            if len(self.rows) > 0 and not isinstance(self.rows[-1], ExitOption):
                self.rows.append(self.exit_option)

            elif len(self.rows) == 0:
                self.rows.append(self.exit_option)

        self.rows[self.selected_row].is_selected = True

        colorpy.hide_cursor()
        self.__render()

        with keyboard.Listener(on_press=self.__on_key_press) as listener:
            listener.join()

        os.system("cls")
        colorpy.show_cursor()

        r = self.rows[self.selected_row]

        if r.callback is not None:
            if r.callback.__code__.co_argcount > 0:
                r.callback(r)

            else:
                r.callback()

        else:
            return r

    def get_longest_option(self) -> List[int]:
        longest = []

        for i in range(len(self.columns)):
            _longest = [self.columns[i]]

            for r in self.rows:
                _longest.append(str(r.row[i] if isinstance(r, OptionRow) else r.name))

            longest.append(len(get_longest(_longest)))

        return longest
