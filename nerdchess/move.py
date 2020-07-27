import copy
from tabulate import tabulate
from abc import ABC, abstractmethod
from nerdchess.config import MOVE_REGEX, letterlist, numbers
from nerdchess import pieces


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
    indices(dict): Origin/destination letter(x)/number(y) mapped to their list
                   position
    """

    def __init__(self, move):
        valid_move = MOVE_REGEX.match(move)
        if not valid_move:
            raise ValueError('Invalid move')

        self.text = move
        self.origin = move[:2]
        self.destination = move[2:]
        self.indices = {
            'or': {
                'x': letterlist.index(self.origin[0]),
                'y': numbers.index(int(self.origin[1]))
            },
            'dest': {
                'x': letterlist.index(self.destination[0]),
                'y': numbers.index(int(self.destination[1]))
            }
        }
        (self.horizontal,
         self.vertical) = self.get_steps()

    @classmethod
    def from_position(cls, position, steps):
        """
        Create a move based on the current position and steps (hori/verti).

        Parameters:
        position(String): The current position (eg. a1)
        steps(tuple(int, int)): The steps taken in the move

        Returns:
        Move: A new move instance
        """
        (letter_steps, number_steps) = steps
        current_letter_index = letterlist.index(position[0])
        current_number_index = numbers.index(int(position[1]))

        new_letter = letterlist[current_letter_index + letter_steps]
        new_number = numbers[current_number_index + number_steps]

        move = "{}{}{}".format(position, new_letter, new_number)
        return cls(move)

    def squares_between(self):
        """ Return the squares between the origin and destination. """
        squares = []

        if self.horizontal == 1 or self.vertical == 1:
            return squares

        if self.is_diagonal():
            steps = 1 if self.horizontal > 0 else -1
            for i in range(steps, self.horizontal, steps):
                letter = letterlist[self.indices['or']['x'] + i]
                number = numbers[self.indices['or']['y'] + i]
                square = f"{letter}{number}"
                squares.append(square)
        elif self.is_horizontal():
            steps = 1 if self.horizontal > 0 else -1
            for i in range(steps, self.horizontal, steps):
                letter = letterlist[self.indices['or']['x'] + i]
                number = self.origin[1]
                square = f"{letter}{number}"
                squares.append(square)
        elif self.is_vertical():
            steps = 1 if self.vertical > 0 else -1
            for i in range(steps, self.vertical, steps):
                letter = self.origin[0]
                number = numbers[self.indices['or']['y'] + i]
                square = f"{letter}{number}"
                squares.append(square)

        return squares

    def is_diagonal(self):
        """ Is the move diagonal? """
        if self.horizontal == 0 or self.vertical == 0:
            return False
        if not abs(self.horizontal) == abs(self.vertical):
            return False
        return True

    def is_horizontal(self):
        """ Is the move horizontal (only)? """
        if self.horizontal == 0:
            return False
        if self.vertical != 0:
            return False
        return True

    def is_vertical(self):
        """ Is the move vertical (only)? """
        if self.vertical == 0:
            return False
        if self.horizontal != 0:
            return False
        return True

    def get_steps(self):
        """ Return the horizontal/vertical steps of the move. """
        horizontal_steps = self.indices['dest']['x'] - \
            self.indices['or']['x']
        vertical_steps = self.indices['dest']['y'] - \
            self.indices['or']['y']

        return (horizontal_steps, vertical_steps)

    def __eq__(self, item):
        """ Describes how to compare a Move. """
        if isinstance(item, Move):
            return self.text == item.text
        try:
            return self.text == str(item)
        except TypeError:
            return NotImplemented

    def __str__(self):
        """ String representation of a Move. """
        return self.text


# TODO Make something like an enumerator with boardrules.
# Maybe an enumerator that loops over functions if that works.
class BoardMove(Move):
    """
    Represents a move in the context of a board.
    Inherits base class (Move) attributes.
    """

    def get_origin_destination(self, board):
        """
        Get the origin and destination square of a move.

        Paramters:
        move(Move): The move to get the squares for

        Returns:
        tuple(Square, Square): The origin and destination
        """
        o_letter = str(self.origin[0])
        o_number = int(self.origin[1])

        d_letter = str(self.destination[0])
        d_number = int(self.destination[1])

        origin = board.squares[o_letter][o_number]
        destination = board.squares[d_letter][d_number]

        return (origin, destination)

    # TODO Expand this function with more boardrules to complete the base game!
    def legal_move(self, board):
        """Checks if a move is legal in the context of the board.

        Parameters:
            board: The board to test the move against
            piece: The piece that's being moved

        Returns:
            Bool: Is the move legal?
        """
        (origin, destination) = self.get_origin_destination(board)
        piece = origin.occupant

        if Move(self.text) not in piece.allowed_moves():
            return False

        # Pawn rules
        if isinstance(piece, pieces.Pawn):
            # Capturing pawn rules
            if self.horizontal == 1:
                # If we're going horizontal, are we at least capturing?
                if not destination.occupant:
                    d_letter = self.destination[0]
                    o_number = int(self.origin[1])
                    # If not, is it at least en passant?
                    if not isinstance(
                            board.squares[d_letter][o_number].occupant,
                            pieces.Pawn):
                        return False
        # Blocking lines
        if not isinstance(piece, pieces.Knight):
            for square in self.squares_between():
                c = square[0]
                i = int(square[1])
                if board.squares[c][i].occupant:
                    return False
        # TODO Castling?

        return True

    def new_board(self, board):
        """Create a new board from the current move and a board.

        This does not do any explicit validation on the move.

        Parameters:
            board: The board to process the current move on

        Returns:
            newboard: The new board
        """
        newboard = copy.deepcopy(board)
        (origin, destination) = self.get_origin_destination(newboard)

        piece = origin.occupant

        origin.occupant = None
        if destination.occupant:
            destination.occupant.captured = True
        destination.occupant = piece
        piece.position = destination.selector

        return newboard

    def process(self, board):
        """Process a move in the context of a board.

        Parameters:
            board: The board to execute on

        Returns:
            Bool: False if the move is incorrect
            Board: A new board
        """
        (origin, destination) = self.get_origin_destination(board)
        piece = origin.occupant

        if not piece:
            return False

        if Move(self.text) not in piece.allowed_moves():
            return False

        # TODO replace with boardrules class
        if not self.legal_move(board):
            return False

        newboard = self.new_board(board)
        if newboard.is_check() == piece.color:
            return False

        return newboard
