import string
from nerdchess import pieces
from nerdchess.config import colors, letters, MOVE_REGEX


class Board():
    """
    Represents a board in a game of chess.

    Attributes:
    letters(list): The letters of a board
    numbers(list): The numbers of a board
    board(dict): A dict of letters containing numbers with squares

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
        self.board = {}
        self.create_board()

    def get_origin_destination(self, move):
        """
        Get the origin and destination square of a move.

        Paramters:
        move(Move): The move to get the squares for

        Returns:
        tuple(Square, Square): The origin and destination
        """
        o_letter = str(move.origin[0])
        o_number = int(move.origin[1])

        d_letter = str(move.destination[0])
        d_number = int(move.destination[1])

        origin = self.board[o_letter][o_number]
        destination = self.board[d_letter][d_number]

        return (origin, destination)

    def legal_move(self, move, piece):
        """
        Checks if a move is legal in the context of the board.

        Parameters:
        move(Move): The move to check
        piece(Piece): The piece that's being moved

        Returns:
        Bool: Is the move legal?
        """
        (origin, destination) = self.get_origin_destination(move)

        # Pawn rules
        if isinstance(piece, pieces.Pawn):
            # Capturing pawn rules
            if move.horizontal == 1:
                if not destination.occupant:
                    return False
        # Blocking lines
        if not isinstance(piece, pieces.Knight):
            # TODO block lines
            # Get squares between origin destination
            squares_between = move.squares_between()
        return True

    def process_move(self, move):
        """
        Process a move on the board, if the piece allows it.

        Parameters:
        move(Move): The move to process

        Returns:
        Bool: Did the move succeed?
        """
        (origin, destination) = self.get_origin_destination(move)

        if not origin.occupant:
            return False

        piece = origin.occupant
        if move not in piece.allowed_moves():
            return False

        if not self.legal_move(move, piece):
            return False

        origin.occupant = None
        if destination.occupant:
            destination.occupant.captured = True
        destination.occupant = piece
        piece.position = destination.selector

        return True

    def matrix(self):
        """ Returns a matrix of the board represented as list. """
        matrix = []

        for i in reversed(self.numbers):
            row = []
            row.append(str(i))

            for letter in self.letters:
                row.append(str(self.board[letter][i]))

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

    def setup_pieces(self, game_pieces):
        """
        Sets up the pieces on the board.

        Parameters:
        game_pieces(list): The pieces to set up
        """
        for piece in game_pieces:
            row = 1 if piece.color == colors.WHITE else 8

            for letter in self.letters:
                square = self.board[letter][row]
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
                square = self.board[letter][row]

                if not square.occupant:
                    square.occupant = pawn
                    pawn.position = square.selector
                    break

    def create_board(self):
        """ Create the board. """
        for letter in self.letters:
            self.board[letter] = {}

            for number in self.numbers:
                selector = "{}{}".format(letter, number)
                self.board[letter][number] = Square(selector)


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
