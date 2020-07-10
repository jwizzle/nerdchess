from abc import ABC, abstractmethod
from enum import Enum
from config import colors


class Piece(ABC):

    def __init__(self, color, captured=False):
        self.color = color
        self.position = ''
        self.captured = captured

    @abstractmethod
    def start_position(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Pawn(Piece):

    def move(self):
        pass

    def __str__(self):
        if self.color == colors.WHITE:
            return u'\u2659'
        else:
            return u'\u265F'

    def start_position(self):
        pass


class Rook(Piece):

    def move(self):
        pass

    def __str__(self):
        if self.color == colors.WHITE:
            return u'\u2656'
        else:
            return u'\u265C'

    def start_position(self):
        if self.color == colors.BLACK:
            return ('a8', 'h8')
        else:
            return ('a1', 'h1')


class Bishop(Piece):

    def move(self):
        pass

    def __str__(self):
        if self.color == colors.WHITE:
            return u'\u2657'
        else:
            return u'\u265D'

    def start_position(self):
        if self.color == colors.BLACK:
            return ('c8', 'f8')
        else:
            return ('c1', 'f1')


class Knight(Piece):

    def move(self):
        pass

    def __str__(self):
        if self.color == colors.WHITE:
            return u'\u2658'
        else:
            return u'\u265E'

    def start_position(self):
        if self.color == colors.BLACK:
            return ('b8', 'g8')
        else:
            return ('b1', 'g1')


class Queen(Piece):

    def move(self):
        pass

    def __str__(self):
        if self.color == colors.WHITE:
            return u'\u2655'
        else:
            return u'\u265B'

    def start_position(self):
        if self.color == colors.BLACK:
            return 'e8'
        else:
            return 'd1'


class King(Piece):

    def move(self):
        pass

    def __str__(self):
        if self.color == colors.WHITE:
            return u'\u2654'
        else:
            return u'\u265A'

    def start_position(self):
        if self.color == colors.BLACK:
            return 'd8'
        else:
            return 'e1'
