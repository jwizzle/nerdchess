"""Holds classes related to interaction with the game back-end."""
# TODO Figure out what exactly we want this to do
# It seems like the best way to implement promotion to construct some
# Types that represent how we interact with the game.
# Eventually we'll also want to do things like reveal options by talking
# Too the same game object instead of querying objects directly and accessing
# Game objects directly from outside the scope of this package.
# Probably want to generate some api spec.
from abc import ABC


class GameEvent(ABC):
    """Generic class for game events."""

    def __init__(self):
        """Construct the event."""
        pass


class Post(GameEvent):
    """Post event used to interact with the game."""

    def __init__(self, action, args):
        """Construct the post."""
        pass
