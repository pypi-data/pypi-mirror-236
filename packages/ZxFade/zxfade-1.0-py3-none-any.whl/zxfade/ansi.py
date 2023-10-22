from typing import LiteralString


__all__ = ['FG_COLOR', 'BG_COLOR', 'RESET',
           'CLEAR', 'TITLE', 'CURSOR',
           'NO_CURSOR']

FG_COLOR: LiteralString = '\x1b[38;2;{};{};{}m'
BG_COLOR: LiteralString = '\x1b[48;2;{};{};{}m'
RESET: LiteralString = '\x1b[0m'
CLEAR: LiteralString = '\x1b[2J\x1b[H'
TITLE: LiteralString = '\x1b]O;{}\a'
CURSOR: LiteralString = '\x1b[?25h'
NO_CURSOR: LiteralString = '\x1b[?25l'