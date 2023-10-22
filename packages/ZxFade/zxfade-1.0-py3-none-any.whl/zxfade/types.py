from typing import TypeVar, Literal, TypeAlias, LiteralString


__all__ = ['AnyStringT', 'FadeDirection']


AnyStringT = TypeVar('AnyStringT', str, LiteralString)
FadeDirection: TypeAlias = Literal['horizontal', 'vertical']