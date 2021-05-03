# Test the constructor and methods of the Tiles class.
from board import Board
from tiles import Tiles


def test_constructor():
    """Test the constructor."""
    WIDTH = 500
    HEIGHT = 500
    SPACING = 50
    TILES_DIMENS = 10
    tiles1 = Tiles(WIDTH, HEIGHT, SPACING, TILES_DIMENS)

    assert tiles1.WIDTH == 500
    assert tiles1.HEIGHT == 500
    assert tiles1.SPACING == 50
    assert tiles1.shift == 25
    assert tiles1.TILES_DIMENS == 10
    assert tiles1.done_initial is False
    assert tiles1.bk_tiles == 0
    assert tiles1.wt_tiles == 0
    for i in range(1, HEIGHT // SPACING + 1):
        for j in range(1, WIDTH // SPACING + 1):
            tile = tiles1.all_tiles[i - 1][j - 1]
            assert tile.color == "blank"
            assert tile.y == SPACING * i - tiles1.shift
            assert tile.x == SPACING * j - tiles1.shift
            assert tile.diameter == 90


def test_initial_tiles():
    """Test the initial_tiles method."""
    tiles1 = Tiles(500, 500, 50, 10)
    tiles1.initial_tiles(tiles1.done_initial)
    assert tiles1.all_tiles[4][5].color == "black"
    assert tiles1.all_tiles[5][4].color == "black"
    assert tiles1.all_tiles[4][4].color == "white"
    assert tiles1.all_tiles[5][5].color == "white"
    assert tiles1.done_initial is True
    tiles1.all_tiles[4][5].color = "white"
    tiles1.initial_tiles(tiles1.done_initial)  # Checks this is done only once.
    assert tiles1.all_tiles[4][5].color == "white"  # Update carries over.


def test_update_color():
    """Test the update color method."""
    tiles1 = Tiles(500, 500, 50, 10)
    assert tiles1.all_tiles[0][0].color == "blank"
    assert tiles1.all_tiles[1][1].color == "blank"
    tiles1.update_color(0, 0, "white")
    tiles1.update_color(1, 1, "black")
    assert tiles1.all_tiles[0][0].color == "white"
    assert tiles1.all_tiles[1][1].color == "black"


def test_generate_legal_moves():
    """Test the generate legal moves"""
    tiles1 = Tiles(400, 400, 100, 4)
    tiles1.initial_tiles(tiles1.done_initial)
    tiles1.generate_legal_moves()
    keys = tiles1.legal_moves.keys()
    assert (0, 1) in keys
    assert (1, 0) in keys
    assert (3, 2) in keys
    assert (2, 3) in keys
    assert len(tiles1.legal_moves[(0, 1)]) == 1
    assert len(tiles1.legal_moves[(1, 0)]) == 1
    assert len(tiles1.legal_moves[(3, 2)]) == 1
    assert len(tiles1.legal_moves[(2, 3)]) == 1

    tiles1.place_black = not tiles1.place_black
    tiles1.generate_legal_moves()
    keys = tiles1.legal_moves.keys()
    assert (2, 0) in keys
    assert (3, 1) in keys
    assert (0, 2) in keys
    assert (1, 3) in keys


def test_check_each_lane():
    """Test the check each lane method"""
    tiles1 = Tiles(400, 400, 100, 4)
    tiles1.initial_tiles(tiles1.done_initial)

    # Check an assumed legal move.
    potential_tile = tiles1.all_tiles[0][1]
    tiles1.check_each_lane(potential_tile, 0, 1, "row")
    assert tiles1.flip_set == set()
    tiles1.check_each_lane(potential_tile, 0, 1, "column")
    assert tiles1.flip_set == {(1, 1)}
    tiles1.check_each_lane(potential_tile, 0, 1, "tl_diag")
    assert tiles1.flip_set == {(1, 1)}
    tiles1.check_each_lane(potential_tile, 0, 1, "tr_diag")
    assert tiles1.flip_set == {(1, 1)}
    tiles1.flip_set = set()  # Refresh for testing.

    # Check an assumed non-legal move.
    potential_tile = tiles1.all_tiles[0][0]
    tiles1.check_each_lane(potential_tile, 0, 0, "row")
    assert tiles1.flip_set == set()
    tiles1.check_each_lane(potential_tile, 0, 0, "column")
    assert tiles1.flip_set == set()
    tiles1.check_each_lane(potential_tile, 0, 0, "tl_diag")
    assert tiles1.flip_set == set()
    tiles1.check_each_lane(potential_tile, 0, 0, "tr_diag")
    assert tiles1.flip_set == set()


def test_check_tile():
    """Test the check tile method."""
    tiles1 = Tiles(400, 400, 100, 4)
    tiles1.initial_tiles(tiles1.done_initial)
    assert tiles1.check_tile(0, 0, []) is False
    assert tiles1.check_tile(1, 1, []) == (1, 1)
    assert tiles1.check_tile(1, 2, {(1, 1)}) is False
    assert tiles1.flip_set == {(1, 1)}
