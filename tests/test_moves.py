import pytest
from tabulate import tabulate
from nerdchess.board import Board
from nerdchess.move import Move, BoardMove
from nerdchess.game import ChessGame
from nerdchess import pieces
from nerdchess.config import colors


@pytest.fixture
def board_queen_e4(board_fixt):
    """ Empty board with queen on e4. """
    board_fixt.place_piece(pieces.Queen(colors.WHITE), 'e4')
    return board_fixt.board


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


class TestBoardRules():
    """ Test specific board rules defined in legal_move(). """

    def test_pawncapture(self, board_fixt):
        """ Test the possibility for pawns to move horizontally. """
        move = BoardMove('e4f5')
        board_fixt.place_piece(pieces.Pawn(colors.WHITE), 'e4')
        board_fixt.place_piece(pieces.Rook(colors.BLACK), 'f5')

        valid = move.process(board_fixt.board)

        assert valid
        assert isinstance(
            valid.squares['f'][5].occupant, pieces.Pawn)

    @pytest.mark.parametrize("black_pos,expected", [
        ('d2', True),
        ('d4', False),
    ])
    def test_enpassant(self, board_fixt, black_pos, expected):
        """ Test enpassant rules. """
        move = BoardMove('c2d3')
        move_piece = pieces.Pawn(colors.WHITE)

        board_fixt.place_piece(move_piece, 'c2')
        board_fixt.place_piece(pieces.Pawn(colors.BLACK), black_pos)

        result = move.legal_move(board_fixt.board)

        assert result == expected

    def test_blocked(self, board_fixt):
        """ Test rules for blocked pieces work correctly. """
        board = board_fixt.default_setup()
        move = BoardMove('c1f4')
        valid = move.process(board)
        assert not valid

    @pytest.mark.parametrize("move,expected", [
        ('f5e7', False),
        ('e4d4', Board),
    ])
    def test_selfchecking(self, board_fixt, move, expected):
        """ Confirm it's not possible to place self in check. """
        board_fixt.place_piece(pieces.King(colors.WHITE), 'e4')
        board_fixt.place_piece(pieces.Knight(colors.WHITE), 'f5')
        board_fixt.place_piece(pieces.Queen(colors.BLACK), 'g6')
        boardmove = BoardMove(move)
        result = boardmove.process(board_fixt.board)

        if isinstance(expected, bool):
            assert result == expected
        else:
            assert isinstance(result, expected)
