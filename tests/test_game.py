import pytest
from nerdchess.game import Player, ChessGame


@pytest.fixture(scope='class')
def chessgame():
    game = ChessGame('blaat', 'henk', 'r')

    return game


class TestGame():
    """
    Tests the setup and basic functionality of a game.
    """

    def test_creation(self, chessgame):
        """ Test for expected contents of the game. """
        assert isinstance(chessgame.player_1, Player)
