# Test the Tile class
from tile import Tile


def test_constructor():
    """Test the constructors for Tile"""
    tile1 = Tile((150, 250), "black", 150)
    assert tile1.color == "black"
    assert tile1.x == 150
    assert tile1.y == 250
    assert tile1.diameter == 140

    tile2 = Tile((30, 100))
    assert tile2.color == "blank"
    assert tile2.x == 30
    assert tile2.y == 100
    assert tile2.diameter == 90
