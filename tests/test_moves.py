import pytest
from tabulate import tabulate
from nerdchess.board import Board
from nerdchess.move import Move
from nerdchess.game import ChessGame
from nerdchess import pieces


@pytest.fixture(params=['e2e4', 'd2d4'])
def move(request):
    move = Move(request.param)
    return move


@pytest.fixture
def board():
    board = Board()
    pieceset = pieces.create_pieces()
    pawnset = pieces.create_pawns()
    board.setup_board(pieceset, pawnset)
    return board


class TestMoves():

    def test_moves(self, move):
        print(move)
