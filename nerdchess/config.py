from enum import Enum
import re


class colors(Enum):
    WHITE = 'w'
    BLACK = 'b'


class letters(Enum):
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'


MOVE_REGEX = re.compile(r"[a-h][1-8][a-h][1-8]")
numbers = range(1, 9)
letterlist = [i.value for i in letters]
