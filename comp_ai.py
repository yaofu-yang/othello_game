# Simulate the AI player in the Othello game
from random import randrange


class CompAI:
    """
    Simulates the computer player in the Othello game.

    Attributes
    ----------
    tiles: instance of the Tiles class.
        Instance of the Tiles class for all the tiles on the board.

    Methods
    -------
    choose_move
        Choose a random tile from the dictionary of legal moves and returns the
        coordinates of the tile as a tuple.
    """
    def __init__(self, tiles):
        """
        Parameters
        ----------
        tiles : instance of Tiles class.
            Instance of the Tiles class for all the tiles on the board.
        """
        self.tiles = tiles

    def choose_move(self):
        """
        Choose a random tile from the dictionary of legal moves and returns the
        coordinates of the tile as a tuple.
        """
        keys = list(self.tiles.legal_moves)  # Captures keys in a list.
        return keys[randrange(0, len(keys))]
