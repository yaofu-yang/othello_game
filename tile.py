# Creates an instance of the Tile class with specified coordinates and color.


class Tile:
    """
    Creates an instance simulating a tile piece on the board in Othello.

    Attributes
    ----------
    color : str
        Color of the tile
    x : int
        x-coordinate of the tile
    y : int
        y-coordinate of the tile
    diameter : int
        diameter of the tile

    Methods
    -------
    display()
        If colored, draws the tile onto its constructed coordinates.
    """
    def __init__(self, coordinates, color="blank", spacing=100):
        """
        Parameters
        -----------
        coordinates : tuple
            Contains the x/y coordinates of the tile, in pixels.
        color : str (default blank)
            Specifies the color of the tile.
        spacing : int (default 100)
            Spacing of each tile on the board.
        """
        self.color = color
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.diameter = spacing - 10

    def display(self):
        """If colored, draws the tile onto its constructed coordinates."""
        WHITE = 255
        BLACK = 0
        if self.color == "blank":
            return

        stroke(0)
        if self.color == "white":
            fill(WHITE)
        elif self.color == "black":
            fill(BLACK)
        ellipse(self.x, self.y, self.diameter, self.diameter)
