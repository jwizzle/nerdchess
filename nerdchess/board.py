import string
from nerdchess import pieces
from nerdchess.config import colors, letters, MOVE_REGEX


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

    def place_piecepawn(self, piece, position):
        """
        Place a piece or pawn on the board.
        Mostly used for testing setups.
        """
        letter = position[0]
        number = int(position[1])
        self.squares[letter][number].occupant = piece
        piece.position = position

    def setup_pieces(self, game_pieces):
        """
        Sets up the pieces on the board.

        Parameters:
        game_pieces(list): The pieces to set up
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
        """
        Sets up the pawns on the board.

        Parameters:
        pawns(list): A list of pawns to set up
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


class Square():
    """
    Represents a square on a chessboard.

    Parameters:
    selector(String): A selector of the square (eg. a1)
    occupant(NoneType): Usually a piece or pawn, needs to have __str__
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
