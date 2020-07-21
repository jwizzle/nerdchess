import pytest


@pytest.fixture(scope='class')
def chessgame():
    from nerdchess.game import ChessGame

    game = ChessGame('blaat', 'henk', 'r')

    return game
