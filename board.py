# Creates an instance representing a board for othello.
from tiles import Tiles
from comp_ai import CompAI


class Board:
    """
    Simulates the board for an Othello game with correct tile placement.

    Attributes
    ----------
    WIDTH : int
        Width of the board, in pixels.
    HEIGHT : int
        Height of the board, in pixels.
    TILES_DIMENS : int
        Number of tiles per side of the square board.
    TOTAL_TILES : int
        Total number of tiles on the board.
    SPACING : int
        Width of each tile, in pixels.
    place_black : Bool
        Conditional for player's turn vs computer's turn.
    gc : Instance from GameController class.
        Maintains the state of the game.
    tiles : instance from Tiles class.
        Manages state of all Tile instances on the board.
    ai : instance from CompAI class
        Maintains behavior from computer player.
    print_user_message : Bool
        Conditional for printing the user's turn message.
    print_comp_message : Bool
        Conditional for printing the computer's turn message.
    game_over : Bool
        Conditional for end-game scenario
    no_legal_move_count = int
        Tallies consecutive cases of no legal moves
    computer_thinking_time = int
        Delay to computer's move (in seconds)
    frames = int
        Number of frames before computer makes move.

    Methods
    -------
    place_tile
        Given the row_index and col_index, update the corresponding tile with
        the correct color based on the turn.
    flip_tiles
        Given the key to a dictionary of legal moves, flip the color attributes
        of all of the Tile objects associated with the key to the given color.
    update_message
        Given the player, prints whose turn it is to terminal.
    check_winning_conditions
        Check if either end-game conditions are reached and make appropriate
        updates to the game_controller instance as applicable.
    get_legal_moves
        Generates all of the available legal moves for the current turn.
    print_turns
        Displays the current turn to terminal. Performs computer's turn if
        applicable.
    do_comp_turn
        Perform the computer's turn once enough time has elapsed.
    no_legal_moves
        Scenario where there are no legal moves for the turn. Makes the
        appropriate changes to switch turns.
    update
        Makes necessary updates including checking the winning conditions,
        checking for the correct player's turn, and checking for legal moves.
    display
        Display the board to screen with the necessary updates.

    """
    def __init__(self, WIDTH, HEIGHT, TILES_DIMENS, SPACING, game_controller):
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
        game_controller = GameController instance
            Maintains the state of the game.
        """
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.TILES_DIMENS = TILES_DIMENS
        self.TOTAL_TILES = TILES_DIMENS ** 2
        self.SPACING = SPACING
        self.place_black = True
        self.gc = game_controller
        self.tiles = Tiles(WIDTH, HEIGHT, SPACING, TILES_DIMENS)
        self.ai = CompAI(self.tiles)
        self.print_user_message = True
        self.print_comp_message = False
        self.game_over = False
        self.no_legal_move_count = 0
        self.computer_thinking_time = 2
        self.frames = 0

    def place_tile(self, row, col):
        """
        Given the row_index and col_index, update the corresponding tile with
        the correct color based on the turn.
        """
        RESET = 0
        key = (row, col)
        if key in self.tiles.legal_moves.keys():  # A legal move
            if self.place_black:  # Player's turn
                self.tiles.update_color(row, col, "black")
                self.flip_tiles(key, "black")
                self.update_message("comp")
            else:  # Computer's turn
                self.tiles.update_color(row, col, "white")
                self.flip_tiles(key, "white")
                self.update_message("user")
            self.place_black = not self.place_black
            self.no_legal_move_count = RESET

    def flip_tiles(self, key, color):
        """
        Given the key to a dictionary of legal moves, flip the color attributes
        of all of the Tile objects associated with the key to the given color.
        """
        flip_values = self.tiles.legal_moves[key]
        for value in flip_values:
            row, col = value[0], value[1]
            self.tiles.update_color(row, col, color)
            if color == "black":
                self.tiles.wt_tiles -= 1
            else:
                self.tiles.bk_tiles -= 1

    def update_message(self, player):
        """Given the player, decides which message to print to terminal."""
        if player == "user":
            self.print_user_message = not self.print_user_message
        elif player == "comp":
            self.print_comp_message = not self.print_comp_message

    def check_winning_conditions(self):
        """
        Check if either end-game conditions are reached and make appropriate
        updates to the game_controller instance as applicable.
        """
        NO_MOVE_MAX = 2
        no_legal_moves = self.no_legal_move_count >= NO_MOVE_MAX
        board_is_full = (self.tiles.bk_tiles + self.tiles.wt_tiles ==
                         self.TOTAL_TILES)
        if no_legal_moves or board_is_full:

            if self.tiles.bk_tiles > self.tiles.wt_tiles:
                self.gc.user_wins = True
            elif self.tiles.wt_tiles > self.tiles.bk_tiles:
                self.gc.comp_wins = True
            else:
                self.gc.tie = True
            self.gc.user_score = self.tiles.bk_tiles
            self.gc.comp_score = self.tiles.wt_tiles
            self.game_over = True

    def get_legal_moves(self):
        """Generates all of the available legal moves for the current turn."""
        if self.place_black:
            self.tiles.place_black = True
        else:
            self.tiles.place_black = False
        self.tiles.generate_legal_moves()

    def print_turns(self):
        """
        Displays the current turn to terminal. Performs computer's turn if
        applicable.
        """
        if not self.place_black:
            if self.print_comp_message:
                print("Computer's turn. Thinking...")
                self.update_message("comp")
            self.do_comp_turn()
        else:
            if self.print_user_message:
                print("User's turn. Please choose a move.")
                self.update_message("user")

    def do_comp_turn(self):
        """Perform the computer's turn once enough time has elapsed."""
        RESET = 0
        FRAMES_PER_SECOND = 60
        if self.frames // FRAMES_PER_SECOND >= self.computer_thinking_time:
            coordinates = self.ai.choose_move()
            if coordinates:
                self.place_tile(coordinates[0], coordinates[1])
            self.frames = RESET

    def no_legal_moves(self):
        """
        Scenario where there are no legal moves for the turn. Makes the
        appropriate changes to switch turns.
        """
        print("There are no legal moves on this turn. Switching turns.")
        if self.place_black:
            self.update_message("comp")
        else:
            self.update_message("user")
        self.place_black = not self.place_black
        self.no_legal_move_count += 1

    def update(self):
        """
        Makes necessary updates including checking the winning conditions,
        checking for the correct player's turn, and checking for legal moves.
        """
        self.check_winning_conditions()
        if not self.game_over:  # End-game conditions not met.
            self.get_legal_moves()
            self.print_turns()  # Check if computer's turn.
            if self.tiles.bk_tiles + self.tiles.wt_tiles > 4:
                if not self.tiles.legal_moves:
                    self.no_legal_moves()
        if not self.place_black:  # Only counts when computer's turn.
            self.frames += 1

    def display(self):
        """Display the board to screen with the necessary updates."""
        self.update()
        self.tiles.display()
        stroke(0)
        strokeWeight(2)
        for i in range(1, self.TILES_DIMENS):
            x, y = self.SPACING * i, self.SPACING * i
            line(x, 0, x, self.HEIGHT)
            line(0, y, self.WIDTH, y)
