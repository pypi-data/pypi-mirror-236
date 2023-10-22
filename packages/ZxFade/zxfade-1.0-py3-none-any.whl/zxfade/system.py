import ctypes
from os import name, system
from sys import stdout

from .ansi import *


__all__ = ['sys']



class System:
    windows: bool
    console: int | None
    
    def __init__(self) -> None:
        self.windows = name == 'nt'
        self._cursor = True
        self._title = ''
        self._transparency = -1

        if self.windows:
            self.console = ctypes.windll.kernel32.GetConsoleWindow()
        else:
            self.console = None


    def __del__(self) -> None:
        self.clear()
        self.cursor = True


    @property
    def title(self) -> str:
        return self._title


    @title.setter
    def title(self, value: str) -> None:
        stdout.write(TITLE.format(value))
        self._title = value


    @property
    def size(self) -> tuple[int, int]:
        return self._size


    @size.setter
    def size(self, value: tuple[int, int]) -> None:
        if self.windows:
            system('mode {}, {}'.format(*value))
            self._size = value


    @property
    def cursor(self) -> bool:
        return self._cursor


    @cursor.setter
    def cursor(self, value: bool) -> None:
        stdout.write(CURSOR if value else NO_CURSOR)
        self._cursor = value


    @property
    def transparency(self) -> int:
        return self._transparency


    @transparency.setter
    def transparency(self, value: int) -> None:
        if self.windows:
            ctypes.windll.user32.SetLayeredWindowAttributes(self.console, 0, value, 2)
            self._transparency = value


    def clear(self) -> None:
        stdout.write(CLEAR)
        stdout.flush()


sys: System = System()