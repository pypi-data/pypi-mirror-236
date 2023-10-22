from threading import Thread
from time import sleep
from sys import stdout

from .colors import Color, Fade
from .pattern import Pattern
from .system import sys
from .ansi import CLEAR, RESET


__all__ = ['FadeAnimation', 'PatternAnimation', 'smooth_show', 'printd', 'inputd']


class FadeAnimation:
    banner: str
    fade: Fade

    def __init__(self,
                 banner: str,
                 fade: Fade) -> None:
        self.banner = banner
        self.fade = fade


    def animate(self,
                duration: float | None = None,
                interval: float = 0.05) -> None:
        passed = False
        cursor = sys.cursor
        sys.cursor = False

        def wait():
            nonlocal passed
            if duration:
                sleep(float(duration))
            else:
                input()
            passed = True

        Thread(target=wait).start()
        decal = 0

        while not passed:
            colored = self.fade.colorate(self.banner, decal)
            stdout.write(CLEAR + colored)
            decal += 1
            sleep(interval)

        sys.clear()
        sys.cursor = cursor


    __call__ = animate


class PatternAnimation:
    banner: str
    pattern: Pattern

    def __init__(self,
                 banner: str,
                 pattern: Pattern) -> None:
        self.banner = banner
        self.pattern = pattern


    def animate(self,
                duration: float | None = None,
                interval: float = 0.05) -> None:
        passed = False
        cursor = sys.cursor
        sys.cursor = False

        def wait():
            nonlocal passed
            if duration:
                sleep(float(duration))
            else:
                input()
            passed = True

        Thread(target=wait).start()
        decal = 0

        while not passed:
            colored = self.pattern.colorate(self.banner, decal)
            stdout.write(CLEAR + colored)
            decal += 1
            sleep(interval)

        sys.clear()
        sys.cursor = cursor
        stdout.write(RESET)


    __call__ = animate


def smooth_show(wait: bool = False,
                interval: float = 0.005,
                transparency: int = 255) -> None:
    def show():
        for i in range(transparency + 1):
            sys.transparency = i
            sleep(interval)

    if wait:
        show()
    else:
        Thread(target=show).start()


def printd(text: str,
           color: Color | Fade,
           interval: float = 0.02,
           lpadding: int = 0,
           linebreak: bool = True) -> None:
    stdout.write(' ' * lpadding)

    if isinstance(color, Color):
        stdout.write(color.ansi)
        for char in text:
            stdout.write(char)
            stdout.flush()
            sleep(interval)

    elif isinstance(color, Fade):
        fade = Fade(color.colors, color.collength, color.direction)
        fadecolors = fade.getcolors()
        fadecolors += list(reversed(fadecolors))
        colcount = len(fadecolors)

        for i, char in enumerate(text):
            fadecol = fadecolors[i % colcount]
            stdout.write(fadecol.colorate(char))
            stdout.flush()
            sleep(interval)

    if linebreak:
        stdout.write('\n')
    stdout.write(RESET)


def inputd(prompt: str,
           color: Color | Fade,
           resp_color: Color | None = None,
           interval: float = 0.02,
           lpadding: int = 0,
           cursor: bool = True) -> str:
    cursor_state = sys.cursor
    printd(prompt, color, interval, lpadding, False)

    if resp_color:
        stdout.write(resp_color.ansi)

    sys.cursor = cursor
    result = input()
    sys.cursor = cursor_state

    stdout.write(RESET)
    return result