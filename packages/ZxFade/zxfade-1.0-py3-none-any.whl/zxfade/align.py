from os import get_terminal_size

from .colors import rmansi
from .types import *


__all__ = ['ycenter', 'xcenter', 'center']


def ycenter(text: AnyStringT,
            size: int | None = None) -> AnyStringT:
    if size is None:
        size = get_terminal_size().lines

    linecount = len(text.splitlines())
    spaces = (size - linecount) // 2
    return '\n' * spaces + text + '\n' * spaces


def xcenter(text: AnyStringT,
            size: int | None = None,
            absolute: bool = False) -> AnyStringT:
    if size is None:
        size = get_terminal_size().columns

    if absolute:
        return '\n'.join(xcenter(line, size) for line in text.splitlines())

    maxline = max(
        (len(line) for line in rmansi(text).splitlines()),
        default=0
    )

    spaces = (size - maxline) // 2

    return '\n'.join((' ' * spaces) + line
                        for line in text.splitlines())


def center(text: AnyStringT,
           size: tuple[int | None, int | None] | None = None,
           absolute: bool = False) -> AnyStringT:
    if size is None:
        size = (None, None)
    return ycenter(xcenter(text, size[0], absolute), size[1])