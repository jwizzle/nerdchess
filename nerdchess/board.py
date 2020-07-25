import string
from nerdchess.config import colors, letters, MOVE_REGEX
from nerdchess.move import BoardMove
from nerdchess.pieces import King


class Board():
    """
    Represents a board in a game of chess.

    Attributes:
    letters(list): The letters of a board
    numbers(list): The numbers of a board
    squares(dict): A dict of letters containing numbers with squares

    {
        a: {
            1: (Square),
            2: (Square),
            etc...
        },
        b: {
            1: (Square),
            2: (Square),
            etc...
        }
        etc...
    }
    """

    def __init__(self):
        self.letters = [i.value for i in letters]
        self.numbers = range(1, 9)
        self.squares = {}
        self.create_board()

    @classmethod
    def piece_list(cls, square_dict):
        """Generator to get the current pieces on the board as a list.

        Parameters:
            square_dict: The dictionary of squares to get the list from
        """
        for v in square_dict.values():
            if isinstance(v, dict):
                yield from cls.piece_list(v)
            else:
                if v.occupant:
                    yield v.occupant
                else:
                    pass

    def matrix(self):
        """ Returns a matrix of the board represented as list. """
        matrix = []

        for i in reversed(self.numbers):
            row = []
            row.append(str(i))

            for letter in self.letters:
                row.append(str(self.squares[letter][i]))

            matrix.append(row)

        last_row = []
        last_row.append(' X ')
        for letter in self.letters:
            last_row.append("_{}_".format(letter))

        matrix.append(last_row)

        return matrix

    def setup_board(self, game_pieces, pawns):
        """ Set up the pieces and pawns in one go. """
        self.setup_pieces(game_pieces)
        self.setup_pawns(pawns)

    def place_piece(self, piece, position):
        """
        Place a piece or pawn on the board.
        Mostly used for testing setups.
        """
        letter = position[0]
        number = int(position[1])
        self.squares[letter][number].occupant = piece
        piece.position = position

    def setup_pieces(self, game_pieces):
        """Sets up the pieces on the board.

        Parameters:
            game_pieces: A list of pieces to set up
        """
        for piece in game_pieces:
            row = 1 if piece.color == colors.WHITE else 8

            for letter in self.letters:
                square = self.squares[letter][row]
                if (square.selector in piece.start_position()
                        and not square.occupant):
                    piece.position = square.selector
                    square.occupant = piece
                    break

    def setup_pawns(self, pawns):
        """Sets up the pawns on the board.

        Parameters:
            pawns: A list of pawns to set up
        """
        for pawn in pawns:
            row = 2 if pawn.color == colors.WHITE else 7

            for letter in self.letters:
                square = self.squares[letter][row]

                if not square.occupant:
                    square.occupant = pawn
                    pawn.position = square.selector
                    break

    def create_board(self):
        """ Create the board. """
        for letter in self.letters:
            self.squares[letter] = {}

            for number in self.numbers:
                selector = "{}{}".format(letter, number)
                self.squares[letter][number] = Square(selector)

    def is_check(self):
        """Is one of the kings in check?

        Returns:
            color: The color of the king that is in check or False
        """
        pieces = list(self.piece_list(self.squares))
        for piece in pieces:
            moves = [BoardMove(i.text) for i in piece.allowed_moves()]
            for move in moves:
                (origin,
                 destination) = move.get_origin_destination(self)
                if (isinstance(destination.occupant, King) and
                        destination.occupant.color != origin.occupant.color):
                    return destination.occupant.color

        return False


class Square():
    """Represents a square on a chessboard.

    Parameters:
        selector: A selector of the square (eg. a1)
        occupant: Usually a piece or pawn, needs to have __str__
    """

    def __init__(self, selector, occupant=None):
        self.selector = selector
        self.occupant = occupant

    def __str__(self):
        """ String representation of a square. """
        if self.occupant:
            return "[{}]".format(str(self.occupant))
        else:
            return '[ ]'
