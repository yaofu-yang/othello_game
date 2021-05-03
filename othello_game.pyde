# Runs the othello game.
# Referenced colors from: https://en.wikipedia.org/wiki/Shades_of_green
# Referenced commenting from: https://realpython.com/documenting-python-code/

from board import Board
from game_controller import GameController
from tiles import Tiles
WIDTH = 800
HEIGHT = 800
TILES_DIMENS = 8
SPACING = 100
GREEN = (0, 100, 0)

gc = GameController(WIDTH, HEIGHT)
b = Board(WIDTH, HEIGHT, TILES_DIMENS, SPACING, gc)


def setup():
    size(WIDTH, HEIGHT)


def draw():
    background(*GREEN)
    b.display()
    gc.update()


def mousePressed():
    if b.place_black:
        if b.tiles.legal_moves:
            b.place_tile(mouseY // SPACING, mouseX // SPACING)
