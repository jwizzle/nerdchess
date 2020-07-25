import pytest
from nerdchess.board import Board
from nerdchess.pieces import King, Queen
from nerdchess.config import colors


@pytest.fixture(params=[
    ('e5', colors.BLACK),
    ('f6', False)
])
def board_kingcheck(request):
    """ Board set up for a king to be and not to be in check. """
    (pos, result) = request.param
    board = Board()
    queen = Queen(colors.WHITE)
    king = King(colors.BLACK)

    board.place_piece(queen, 'e4')
    board.place_piece(king, pos)

    return (board, result)


class TestBoard():

    def test_ischeck(self, board_kingcheck):
        (board, result) = board_kingcheck
        assert board.is_check() == result
