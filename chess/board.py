import string
import pieces
from config import colors, letters, MOVE_REGEX


class Board():

    def __init__(self):
        self.letters = [i.value for i in letters]
        self.numbers = range(1, 9)
        self.board = {}
        self.create_board()

    def get_origin_destination(self, move):
        origin = move[:2]
        o_letter = str(origin[0])
        o_number = int(origin[1])

        destination = move[2:]
        d_letter = str(destination[0])
        d_number = int(destination[1])

        origin = self.board[o_letter][o_number]
        destination = self.board[d_letter][d_number]

        return (origin, destination)

    def process_move(self, move):
        valid_move = MOVE_REGEX.match(move)
        if not valid_move:
            return False

        (origin, destination) = self.get_origin_destination(move)

        if not origin.occupant:
            return False

        piece = origin.occupant
        origin.occupant = None
        destination.occupant = piece

        return True

    def matrix(self):
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
        self.setup_pieces(game_pieces)
        self.setup_pawns(pawns)

    def setup_pieces(self, game_pieces):
        for piece in game_pieces:
            row = 1 if piece.color == colors.WHITE else 8

            for letter in self.letters:
                square = self.board[letter][row]
                if (square.selector in piece.start_position()
                        and not square.occupant):
                    square.occupant = piece

    def setup_pawns(self, pawns):
        for pawn in pawns:
            row = 2 if pawn.color == colors.WHITE else 7

            for letter in self.letters:
                square = self.board[letter][row]

                if not square.occupant:
                    square.occupant = pawn
                    break

    def create_board(self):
        for letter in self.letters:
            self.board[letter] = {}

            for number in self.numbers:
                selector = "{}{}".format(letter, number)
                self.board[letter][number] = Square(selector)


class Square():

    def __init__(self, selector, occupant=None):
        self.selector = selector
        self.occupant = occupant

    def __str__(self):
        if self.occupant:
            return "[{}]".format(str(self.occupant))
        else:
            return '[ ]'
