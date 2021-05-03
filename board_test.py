# Test for the Board class
from board import Board
from game_controller import GameController


def test_constructor():
    """Test the attributes"""
    WIDTH = 500
    HEIGHT = 500
    TILES_DIMENS = 10
    SPACING = 50
    g = GameController(WIDTH, HEIGHT)
    board1 = Board(WIDTH, HEIGHT, TILES_DIMENS, SPACING, g)

    assert board1.WIDTH == 500
    assert board1.HEIGHT == 500
    assert board1.TILES_DIMENS == 10
    assert board1.TOTAL_TILES == 100
    assert board1.SPACING == 50
    assert board1.place_black is True
    assert board1.gc is g
    for i in range(board1.TILES_DIMENS):
        assert len(board1.tiles.all_tiles[i]) == board1.TILES_DIMENS
    assert board1.ai.tiles is board1.tiles
    assert board1.print_comp_message is False
    assert board1.print_user_message is True
    assert board1.game_over is False
    assert board1.no_legal_move_count == 0
    assert board1.computer_thinking_time == 2
    assert board1.frames == 0


def test_place_tile():
    """Test place_tile method"""
    WIDTH = 400
    HEIGHT = 400
    TILES_DIMENS = 4
    SPACING = 100
    g = GameController(WIDTH, HEIGHT)
    board1 = Board(WIDTH, HEIGHT, TILES_DIMENS, SPACING, g)

    board1.tiles.initial_tiles(False)
    board1.get_legal_moves()
    keys = board1.tiles.legal_moves.keys()
    assert board1.tiles.all_tiles[0][1].color == "blank"
    assert (0, 1) in keys

    board1.place_tile(0, 1)
    assert board1.tiles.all_tiles[0][1].color == "black"
    assert board1.tiles.bk_tiles == 4
    assert board1.tiles.wt_tiles == 1
    assert board1.place_black is False
    assert board1.print_comp_message is True

    board1.get_legal_moves()
    keys = board1.tiles.legal_moves.keys()
    assert len(keys) == 3
    assert (0, 0) in keys

    board1.place_tile(0, 0)
    assert board1.tiles.all_tiles[0][0].color == "white"
    assert board1.tiles.bk_tiles == 3
    assert board1.tiles.wt_tiles == 3
    assert board1.place_black is True

    board1.get_legal_moves()
    board1.place_tile(0, 0)  # Attempt placing black
    assert board1.tiles.all_tiles[0][0].color == "white"
    assert board1.tiles.bk_tiles == 3
    assert board1.tiles.wt_tiles == 3

    board1.get_legal_moves()
    board1.place_tile(3, 3)  # Placing on illegal space.
    assert board1.tiles.bk_tiles == 3
    assert board1.tiles.wt_tiles == 3


def test_flip_tiles():
    """Test the flip tiles method."""
    g = GameController(400, 400)
    board1 = Board(400, 400, 10, 100, g)
    assert board1.tiles.all_tiles[0][0].color == "blank"
    assert board1.tiles.all_tiles[0][3].color == "blank"
    assert board1.tiles.all_tiles[3][0].color == "blank"
    assert board1.tiles.all_tiles[3][3].color == "blank"
    flip_set = {(0, 0), (0, 3), (3, 3)}
    board1.tiles.legal_moves["key"] = flip_set
    board1.flip_tiles("key", "black")

    assert board1.tiles.all_tiles[0][0].color == "black"
    assert board1.tiles.all_tiles[0][3].color == "black"
    assert board1.tiles.all_tiles[3][0].color == "blank"
    assert board1.tiles.all_tiles[3][3].color == "black"


def test_update_message():
    """Test the update message method."""
    g = GameController(400, 400)
    board1 = Board(400, 400, 10, 100, g)
    assert board1.print_comp_message is False
    assert board1.print_user_message is True
    board1.update_message("user")
    assert board1.print_comp_message is False
    assert board1.print_user_message is False
    board1.update_message("comp")
    assert board1.print_comp_message is True
    assert board1.print_user_message is False


def test_check_winning_conditions():
    """Test the check winning conditions method."""
    WIDTH = 500
    HEIGHT = 500
    TILES_DIMENS = 10
    SPACING = 50
    g = GameController(WIDTH, HEIGHT)
    g2 = GameController(WIDTH, HEIGHT)
    g3 = GameController(WIDTH, HEIGHT)
    board1 = Board(WIDTH, HEIGHT, TILES_DIMENS, SPACING, g)
    board2 = Board(WIDTH, HEIGHT, TILES_DIMENS, SPACING, g2)
    board3 = Board(WIDTH, HEIGHT, TILES_DIMENS, SPACING, g3)

    # Case one - Game ends with all tiles placed.
    board1.tiles.bk_tiles, board1.tiles.wt_tiles = 51, 49
    board1.no_legal_move_count = 0
    board1.check_winning_conditions()
    assert board1.gc.user_wins is True
    assert board1.gc.comp_wins is False
    assert board1.gc.tie is False
    assert board1.gc.user_score == 51
    assert board1.gc.comp_score == 49

    # Case two - Game is still ongoing.
    board2.tiles.bk_tiles, board2.tiles.wt_tiles = 41, 49
    board2.no_legal_move_count = 1
    board2.check_winning_conditions()
    assert board2.gc.user_wins is False
    assert board2.gc.comp_wins is False
    assert board2.gc.tie is False
    assert board2.gc.user_score is 2
    assert board2.gc.comp_score is 2

    # Case three - Game ends without placing all tiles.
    board3.tiles.bk_tiles, board3.tiles.wt_tiles = 0, 78
    board3.no_legal_move_count = 2
    board3.check_winning_conditions()
    assert board3.gc.user_wins is False
    assert board3.gc.comp_wins is True
    assert board3.gc.tie is False
    assert board3.gc.user_score is 0
    assert board3.gc.comp_score is 78


def test_get_legal_moves():
    """Test the get legal moves method"""
    g = GameController(400, 400)
    board1 = Board(400, 400, 4, 100, g)
    board1.tiles.initial_tiles(False)
    assert board1.place_black is True
    board1.get_legal_moves()
    keys = board1.tiles.legal_moves.keys()
    assert (0, 1) in keys
    assert (1, 0) in keys
    assert (2, 3) in keys
    assert (3, 2) in keys


def test_print_turns():
    """Test the print turns method."""
    g = GameController(400, 400)
    board1 = Board(400, 400, 4, 100, g)
    assert board1.print_comp_message is False
    assert board1.print_user_message is True
    assert board1.place_black is True
    board1.print_turns()
    assert board1.print_comp_message is False
    assert board1.print_user_message is False
    board1.print_turns()  # Both messages are currently False
    assert board1.print_comp_message is False
    assert board1.print_user_message is False


def test_do_comp_turn():
    """Test the do comp turn method."""
    g = GameController(400, 400)
    board1 = Board(400, 400, 4, 100, g)
    board1.tiles.initial_tiles(False)
    board1.place_black = False  # To simulate AI turn.
    board1.get_legal_moves()

    board1.frames = 120
    board1.do_comp_turn()
    assert board1.tiles.bk_tiles == 1
    assert board1.tiles.wt_tiles == 4
    assert board1.place_black is True
    assert board1.no_legal_move_count == 0


def test_no_legal_moves():
    """Test the no legal moves method."""
    g = GameController(400, 400)
    board1 = Board(400, 400, 4, 100, g)
    board1.tiles.initial_tiles(False)
    board1.no_legal_moves()
    assert board1.place_black is False
    assert board1.print_comp_message is True
    assert board1.no_legal_move_count == 1
    board1.print_user_message = False

    board1.no_legal_moves()
    assert board1.place_black is True
    assert board1.print_user_message is True
    assert board1.no_legal_move_count == 2


def test_update():
    """Test the update method."""
    g = GameController(400, 400)
    board1 = Board(400, 400, 4, 100, g)
    board1.tiles.initial_tiles(False)
    board1.update()
    assert board1.game_over is False
    assert len(board1.tiles.legal_moves) == 4
    assert board1.print_user_message is False
    assert board1.tiles.bk_tiles + board1.tiles.wt_tiles == 4

    board1.place_tile(1, 0)
    board1.update()
    assert board1.game_over is False
    assert len(board1.tiles.legal_moves) == 3
    assert board1.print_comp_message is False
    assert board1.tiles.bk_tiles + board1.tiles.wt_tiles == 5
    assert board1.frames == 1
