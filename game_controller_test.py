# Test the GameController class.
from game_controller import GameController
from board import Board


def test_constructor():
    """Test the constructor"""
    WIDTH = 500
    HEIGHT = 500
    gc = GameController(WIDTH, HEIGHT)
    assert gc.WIDTH == 500
    assert gc.HEIGHT == 500
    assert gc.comp_wins is False
    assert gc.user_wins is False
    assert gc.tie is False
    assert gc.comp_score is 2
    assert gc.user_score is 2
    assert gc.draw is True


def test_update():
    """Test the update method"""
    WIDTH = 400
    HEIGHT = 400
    TILES_DIMENS = 4
    SPACING = 100
    gc1 = GameController(WIDTH, HEIGHT)
    board = Board(WIDTH, HEIGHT, TILES_DIMENS, SPACING, gc1)
    board.tiles.wt_tiles = 9
    board.tiles.bk_tiles = 7
    board.update()

    assert board.gc.comp_wins is True
    assert board.gc.comp_score == 9
    assert board.gc.user_score == 7
