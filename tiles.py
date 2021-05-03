# Creates an instance of the Tiles class that generates all of the tile objects
# onto the board.
from tile import Tile
from copy import deepcopy


class Tiles:
    """
    Simulates all of the tiles on the board.

    Attributes
    ----------
    WIDTH : int
        Width of the board, in pixels
    HEIGHT : int
        Height of the board, in pixels
    SPACING : int
        Width of each tile, in pixels
    shift : int
        Used for centering each tile piece
    TILES_DIMENS : int
        Amount of tiles per side of the square board
    all_tiles : list of lists of Tile objects
        Completes each row/column of tiles on the board
    done_initial : Bool
        Conditional for initial placement of tiles
    bk_tiles : int
        Counter of black tiles, updated per frame
    wt_tiles : int
        Counter of white tiles, updated per frame
    legal_moves : dict
        key: tuple containing index-coordinates of the target tile.
        value: Set containing the index-coordinates of flippable tiles
        Refreshed per frame.
    flip_set : set
        Contains the index-coordinates of flippable tiles for a legal move.
    place_black : Bool
        Conditional for player's turn vs computer's turn

    Methods
    -------
    display
        Call the display method for each tile.
    initial_tiles
        If not yet completed, place the initial tiles on the board.
    update_color
        Update a tile at the row_index, column_index to color
    generate_legal_moves
        Iterates through every Tile object on the board to check for legal
        moves, also storing the coordinates of flippable tiles per legal move.
    check_each_lane
        Given a tile instance, its row-index, column-index, and the specified
        search lane on the board, updates self.flip_set with the coordinates of
        opponent tiles that will be flipped with this tile placement.
    check_tile
        Given a row_index and column_index, return a tuple containing these
        values if it is an opponent tile. Returns false otherwise.
        Merges flip_set with attribute self.flip_set if applicable.
    """
    def __init__(self, WIDTH, HEIGHT, SPACING, TILES_DIMENS):
        """
        Parameters
        ----------
        WIDTH : int
            Width of the board, in pixels.
        HEIGHT : int
            Height of the board, in pixels.
        SPACING: int
            Width of each tile, in pixels
        TILES_DIMENS : int
            Number of tiles per side of the square board.
        """
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SPACING = SPACING
        self.shift = SPACING // 2
        self.TILES_DIMENS = TILES_DIMENS
        # Initialize a list of lists of tiles objects.
        self.all_tiles = [[Tile((self.SPACING * i - self.shift,
                                 self.SPACING * j - self.shift))
                           for i in range(1, self.WIDTH // self.SPACING + 1)]
                          for j in range(1, self.HEIGHT // self.SPACING + 1)]
        self.done_initial = False
        self.bk_tiles = 0
        self.wt_tiles = 0
        self.legal_moves = {}
        self.flip_set = set()
        self.place_black = True

    def initial_tiles(self, done):
        """If not yet completed, place the initial tiles on the board."""
        if not done:
            midpoint = self.TILES_DIMENS // 2
            for i in range(midpoint - 1, midpoint + 1):
                for j in range(midpoint - 1, midpoint + 1):
                    if (i + j) % 2 == 1:
                        self.update_color(i, j, "black")
                    else:
                        self.update_color(i, j, "white")
            self.done_initial = True

    def update_color(self, row, col, color):
        """Update a tile at the row_index, column_index to color"""
        if color == "black":
            self.bk_tiles += 1
        elif color == "white":
            self.wt_tiles += 1
        self.all_tiles[row][col].color = color

    def generate_legal_moves(self):
        """
        Iterates through every Tile object on the board to check for legal
        moves, also storing the coordinates of flippable tiles per legal move.
        """
        self.legal_moves = {}
        for row in range(self.TILES_DIMENS):
            for col in range(self.TILES_DIMENS):
                potential_tile = self.all_tiles[row][col]
                if potential_tile.color == "blank":  # Otherwise no action.
                    self.check_each_lane(potential_tile, row, col, "row")
                    self.check_each_lane(potential_tile, row, col, "column")
                    self.check_each_lane(potential_tile, row, col, "tl_diag")
                    self.check_each_lane(potential_tile, row, col, "tr_diag")
                    if self.flip_set:
                        self.legal_moves[(row, col)] = deepcopy(self.flip_set)
                    self.flip_set = set()  # Reset for each tile.

    def check_each_lane(self, tile, row, col, lane):
        """
        Given a tile instance, its row-index, column-index, and the specified
        search lane on the board, updates self.flip_set with the coordinates of
        opponent tiles that will be flipped with this tile placement.
        """

        if lane == "row":  # Horizontal lane
            flip_set_one, flip_set_two = set(), set()
            for c in range(1, self.TILES_DIMENS - col):  # Right
                flippable = self.check_tile(row, col + c, flip_set_one)
                if flippable:
                    flip_set_one.add(flippable)
                else:
                    break
            for c in range(col - 1, -1, -1):  # Left
                flippable = self.check_tile(row, c, flip_set_two)
                if flippable:
                    flip_set_two.add(flippable)
                else:
                    break

        elif lane == "column":  # Vertical lane
            flip_set_one, flip_set_two = set(), set()
            for r in range(1, self.TILES_DIMENS - row):  # Top
                flippable = self.check_tile(row + r, col, flip_set_one)
                if flippable:
                    flip_set_one.add(flippable)
                else:
                    break
            for r in range(row - 1, -1, -1):  # Bottom
                flippable = self.check_tile(r, col, flip_set_two)
                if flippable:
                    flip_set_two.add(flippable)
                else:
                    break

        elif lane == "tl_diag":  # Diagonal reaching top left.
            flip_set_one, flip_set_two = set(), set()
            upper_bound = max(row, col)
            lower_bound = min(row, col)
            for i in range(1, self.TILES_DIMENS - upper_bound):  # Bottom right
                flippable = self.check_tile(row + i, col + i, flip_set_one)
                if flippable:
                    flip_set_one.add(flippable)
                else:
                    break
            for i in range(1, lower_bound + 1):  # Top left
                flippable = self.check_tile(row - i, col - i, flip_set_two)
                if flippable:
                    flip_set_two.add(flippable)
                else:
                    break

        elif lane == "tr_diag":  # Diagonal reaching top right.
            flip_set_one, flip_set_two = set(), set()
            bound_one = min(row + 1, self.TILES_DIMENS - col)
            bound_two = min(self.TILES_DIMENS - row, col + 1)
            for i in range(1, bound_one):  # Top right
                flippable = self.check_tile(row - i, col + i, flip_set_one)
                if flippable:
                    flip_set_one.add(flippable)
                else:
                    break
            for i in range(1, bound_two):  # Bottom left
                flippable = self.check_tile(row + i, col - i, flip_set_two)
                if flippable:
                    flip_set_two.add(flippable)
                else:
                    break

    def check_tile(self, r, c, flip_set):
        """
        Given a row_index and column_index, return a tuple containing these
        values if it is an opponent tile. Returns false otherwise.
        Merges flip_set with attribute self.flip_set if applicable.
        """
        if self.place_black:
            opponent_color, current_color = "white", "black"
        else:
            opponent_color, current_color = "black", "white"

        if self.all_tiles[r][c].color == opponent_color:  # flip candidate.
            row = self.all_tiles[r][c].y // self.SPACING
            col = self.all_tiles[r][c].x // self.SPACING
            coordinates = (row, col)
            return coordinates
        elif self.all_tiles[r][c].color == current_color:
            if flip_set:
                self.flip_set = self.flip_set.union(flip_set)
            return False
        else:  # Next is blank.
            return False

    def display(self):
        """Call the display method for each tile."""
        self.initial_tiles(self.done_initial)
        for i in range(self.TILES_DIMENS):
            for j in range(self.TILES_DIMENS):
                self.all_tiles[i][j].display()
