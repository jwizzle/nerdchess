import random
from nerdchess import pieces
from nerdchess.board import Board
from nerdchess.config import colors
from nerdchess.move import Move


class Player():
    """ 
    Represents a player in a chessgame.

    Parameters: 
    name(String): The name of the player
    color(colors): The color of the player
    turn(Bool): Whether it's the players turn

    Attributes:
    name(String): The name of the player
    color(colors): The color of the player
    turn(Bool): Is it the players turn?
    """

    def __init__(self, name, color, turn=True):
        self.name = name
        self.color = color
        self.turn = turn

    def __str__(self):
        """ String representation of a player. """
        return "{}, playing {}.".format(self.name, self.color)


class ChessGame():
    """
    Creates a new chessgame with players, pieces, and sets up the board.

    Parameters:
    name_1(String): The name of player 1
    name_2(String): The name of player 2
    color_input(colors): The color for player 1
    over(Bool): Whether the game is over

    Attributes:
    player_1(Player): Player 1
    player_2(Player): Player 2
    playerlist(list): A list of the two players
    board(Board): The board the game is played on
    pieces(list): A list of the pieces the game is played with
    pawns(list): A list of the pawns the game is played with
    """

    def __init__(self, name_1, name_2, color_input, over=False):
        (self.player_1,
         self.player_2) = self.create_players(name_1, name_2, color_input)
        self.playerlist = [self.player_1, self.player_2]

        self.board = Board()
        self.pieces = self.create_pieces()
        self.pawns = self.create_pawns()
        self.board.setup_board(self.pieces, self.pawns)
        self.over = over

    def pass_turn(self):
        """ Passes the turn to the other player. """
        for player in self.playerlist:
            player.turn = False if player.turn else True

    def move(self, player, move):
        """
        Process the move in a game of chess.

        Parameters:
        player(Player): The player that made the move
        move(String): The move representeed by squares (eg. e2e4)

        Returns:
        Bool: Was the move succesful?
        """
        move = Move(move)

        (origin, destination) = self.board.get_origin_destination(move)

        if origin.occupant:
            if origin.occupant.color != player.color:
                return False
        else:
            return False

        result = self.board.process_move(move)
        if result:
            self.pass_turn()

        return result

    def create_pieces(self):
        """ Create chesspieces used in the game. """
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
        """ Create pawns used in the game. """
        pawns = []

        for color in colors:
            for letter in self.board.letters:
                pawns.append(pieces.Pawn(color))

        return pawns

    def create_players(self, name_1, name_2, color_input):
        """
        Creates two players and bases the colors off of the one assigned to 1.

        Parameters:
        name_1(String): The name of player 1
        name_2(String): The name of player 2
        color_input(String): The color to assign to player 1

        Returns:
        Tuple(Player, Player): The players that are going to play the game
        """
        if color_input == 'r':
            color = self.random_color()
            turn = True if color == colors.WHITE else False
            player_1 = Player(name_1, color, turn)
        elif color_input == colors.WHITE.value:
            player_1 = Player(name_1, colors.WHITE)
        elif color_input == colors.BLACK.value:
            player_1 = Player(name_1, colors.BLACK, False)
        else:
            raise ValueError('Wrong color input.')

        player_2_color = (colors.WHITE if player_1.color == colors.BLACK
                          else colors.BLACK)

        turn = True if player_2_color == colors.WHITE else False
        player_2 = Player(name_2, player_2_color, turn)

        return (player_1, player_2)

    def random_color(self):
        """ Return a random color. """
        if bool(random.getrandbits(1)):
            return colors.WHITE
        else:
            return colors.BLACK
