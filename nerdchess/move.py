from abc import ABC
from config import MOVE_REGEX, letterlist, numbers


class Move(ABC):
    """
    Represents a move in a game of chess.

    Parameters:
    move(String): A string that's tested with the regex '[a-h][1-8][a-h][1-8]'

    Attributes:
    text(String): String representation of the move r'[a-h][1-8][a-h][1-8]'
    origin(String): String representation of the origin square
    destination(String): String representation of the destination square
    horizontal(int): Amount of horizontal steps in the move
    vertical(int): Amount of vertical steps in the move
    """

    def __init__(self, move):
        valid_move = MOVE_REGEX.match(move)
        if not valid_move:
            raise ValueError('Invalid move')

        self.text = move
        self.origin = move[:2]
        self.destination = move[2:]
        (self.horizontal,
         self.vertical) = self.get_steps()

    @classmethod
    def from_position(cls, position, steps):
        (letter_steps, number_steps) = steps
        current_letter_index = letterlist.index(position[0])
        current_number_index = numbers.index(int(position[1]))

        new_letter = letterlist[current_letter_index + letter_steps]
        new_number = numbers[current_number_index + number_steps]

        move = "{}{}{}".format(position, new_letter, new_number)
        return cls(move)

    def squares_between(self):
        # TODO Make horizontal/vertical steps part of a move
        # Use it to get the squares between a move, return list
        # Don't forget the is_diagonal function
        squares = []

        if self.is_diagonal():
            steps = 1 if self.horizontal > 0 else -1
            for i in range(1, self.horizontal, steps):
                # TODO for every step get a new number/letter
                # TODO maybe think of some way to keep letter/number list index
                # more ready it's being used a lot like in get_steps

                pass

        return squares

    def is_diagonal(self):
        if self.horizontal == 0 or self.vertical == 0:
            return False
        if not abs(self.horizontal) == abs(self.vertical):
            return False
        return True

    def is_horizontal(self):
        if self.horizontal == 0:
            return False
        if self.vertical != 0:
            return False
        return True

    def is_vertical(self):
        if self.vertical == 0:
            return False
        if self.horizontal != 0:
            return False
        return True

    def get_steps(self):
        current_letter_index = letterlist.index(self.origin[0])
        current_number_index = numbers.index(int(self.origin[1]))
        dest_letter_index = letterlist.index(self.destination[0])
        dest_number_index = numbers.index(int(self.destination[1]))

        horizontal_steps = dest_letter_index - current_letter_index
        vertical_steps = dest_number_index - current_number_index

        return (horizontal_steps, vertical_steps)

    def __eq__(self, item):
        if isinstance(item, Move):
            return self.text == item.text
        try:
            return self.text == str(item)
        except TypeError:
            return NotImplemented

    def __str__(self):
        return self.text
