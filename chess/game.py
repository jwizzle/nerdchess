import random
import pieces
from board import Board
from config import colors


class Player():

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        return "{}, playing {}.".format(self.name, self.color)


class ChessGame():

    def __init__(self, name_1, name_2, color_input):
        (self.player_white,
         self.player_black) = self.create_players(name_1, name_2, color_input)
        self.playerlist = [self.player_white, self.player_black]

        self.board = Board()
        self.pieces = self.create_pieces()
        self.pawns = self.create_pawns()
        self.board.setup_board(self.pieces, self.pawns)

    def move(self, move):
        result = self.board.process_move(move)
        return result

    def create_pieces(self):
        chess_pieces = []

        for color in colors:
            chess_pieces.append(pieces.Rook(color))
            chess_pieces.append(pieces.Rook(color))
            chess_pieces.append(pieces.Knight(color))
            chess_pieces.append(pieces.Knight(color))
            chess_pieces.append(pieces.Bishop(color))
            chess_pieces.append(pieces.Bishop(color))
            chess_pieces.append(pieces.Queen(color))
            chess_pieces.append(pieces.King(color))

        return chess_pieces

    def create_pawns(self):
        pawns = []

        for color in colors:
            for letter in self.board.letters:
                pawns.append(pieces.Pawn(color))

        return pawns

    def create_players(self, name_1, name_2, color_input):
        if color_input == 'r':
            player_1 = Player(name_1, self.random_color())
        elif color_input == colors.WHITE:
            player_1 = Player(name_1, colors.WHITE)
        elif color_input == colors.BLACK:
            player_1 = Player(name_1, colors.BLACK)
        else:
            exit('Wrong color input, crashing unrecoverably berawawegaw.g...')

        player_2_color = (colors.WHITE if player_1.color == colors.BLACK
                          else colors.BLACK)

        player_2 = Player(name_2, player_2_color)

        return (player_1, player_2)

    def random_color(self):
        if bool(random.getrandbits(1)):
            return colors.WHITE
        else:
            return colors.BLACK
