from enum import Enum
import re


MOVE_REGEX = re.compile(r"[a-h][1-8][a-h][1-8]")


class colors(Enum):
    BLACK = 'b'
    WHITE = 'w'


class letters(Enum):
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
