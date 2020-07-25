import pytest
from nerdchess.board import Board
from nerdchess.pieces import King, Queen
from nerdchess.config import colors


@pytest.fixture(params=[
    ('e5', colors.BLACK),
    ('f6', False)
])
def board_kingcheck(request, board_fixt):
    """ Board set up for a king to be and not to be in check. """
    (pos, result) = request.param
    board_fixt.place_piece(Queen(colors.WHITE), 'e4')
    board_fixt.place_piece(King(colors.BLACK), pos)

    return (board_fixt.board, result)


class TestBoard():
    """ Test aspects of the Board class. """

    def test_ischeck(self, board_kingcheck):
        """ Test if kingcheck works correctly """
        (board, result) = board_kingcheck
        assert board.is_check() == result
