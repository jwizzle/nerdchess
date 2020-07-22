import pytest
from tabulate import tabulate
from nerdchess.board import Board
from nerdchess.move import Move, BoardMove
from nerdchess.game import ChessGame
from nerdchess import pieces
from nerdchess.config import colors


@pytest.fixture
def board_default():
    """ Board set up with default pieces for a new game. """
    board = Board()
    boardpieces = pieces.create_pieces()
    pawns = pieces.create_pawns()
    board.setup_board(boardpieces, pawns)
    return board


@pytest.fixture
def board_queen_e4():
    """ Empty board with queen on e4. """
    board = Board()
    piece = pieces.Queen(colors.WHITE)
    piece.position = 'e4'
    board.squares['e'][4].occupant = piece
    return board


class TestDirections():
    """ Test directional movement with a queen on e4. """

    def test_diagonal(self, board_queen_e4):
        move = BoardMove('e4c2')
        result = move.process(board_queen_e4)

        assert move.squares_between() == ['d3']
        assert result

    def test_horizontal(self, board_queen_e4):
        move = BoardMove('e4a4')
        result = move.process(board_queen_e4)

        assert move.squares_between() == [
            'd4', 'c4', 'b4'
        ]
        assert result

    def test_vertical(self, board_queen_e4):
        move = BoardMove('e4e7')
        result = move.process(board_queen_e4)

        assert move.squares_between() == ['e5', 'e6']
        assert result


@pytest.fixture
def board_pawncapture():
    """ Board set up for a pawn to capture a rook on f5. """
    board = Board()
    pawn = pieces.Pawn(colors.WHITE)
    piece = pieces.Rook(colors.BLACK)

    board.place_piecepawn(pawn, 'e4')
    board.place_piecepawn(piece, 'f5')

    return board


class TestBoardRules():
    """ Test specific board rules defined in legal_move(). """

    def test_pawncapture(self, board_pawncapture):
        """ Test the possibility for pawns to move horizontally. """
        move = BoardMove('e4f5')
        valid = move.process(board_pawncapture)

        assert valid
        assert isinstance(
            board_pawncapture.squares['f'][5].occupant, pieces.Pawn)

    def test_blocked(self, board_default):
        move = BoardMove('c1f4')
        valid = move.process(board_default)
        assert not valid
