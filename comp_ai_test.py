# Test for the CompAI class
from comp_ai import CompAI
from tiles import Tiles


def test_constructor():
    """Test the constructor"""
    tiles = Tiles(400, 400, 100, 4)
    ai = CompAI(tiles)
    assert ai.tiles is tiles


def test_choose_move():
    """Test the choose move method."""
    tiles = Tiles(400, 400, 100, 4)
    ai = CompAI(tiles)
    ai.tiles.initial_tiles(False)
    ai.tiles.generate_legal_moves()
    keys = ai.tiles.legal_moves.keys()
    assert ai.choose_move() in keys