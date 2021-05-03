# Creates an instance of GameController class which maintains the state of
# the Othello game.
from score_organizer import ScoreOrganizer


class GameController:
    """
    Maintains the state of the Othello game.

    Attributes
    ----------
    WIDTH = int
        Width of the board, in pixels
    HEIGHT = int
        Height of the board, in pixels
    draw = Bool
        Conditional to draw to screen or terminal
    updated_score = Bool
        Conditional to ensure score only updates once
    comp_wins = Bool
        Conditional to check if computer wins
    user_wins = Bool
        Conditional to check if user wins
    tie = Bool
        Conditional to check if user and computer ties
    comp_score = int
        Computer's score, only updated at end-game
    user_score = int
        User's score, only updated at end-game
    delay = int
        Counter to delay score update.

    Methods
    -------
    update
        If end-game conditions are reached, displays the winner in the terminal
        and displays the user's total score on the board.
        Updates the score file with the user's name and score.
    write_score
        Continuously prompts the user until an input of at least one character
        is given. Then updates the scores in file "othello.txt"
    input
        Given a string message, initializes a user-interface and displays
        the message to the user. Returns user input as a string.
    """
    def __init__(self, WIDTH, HEIGHT):
        """
        Parameters
        ----------
        WIDTH : int
            Width of the board, in pixels
        HEIGHT: int
            Height of the board, in pixels
        """
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.draw = True
        self.updated_score = False
        self.comp_wins = False
        self.user_wins = False
        self.tie = False
        self.comp_score = 2
        self.user_score = 2
        self.delay = 0

    def update(self):
        """
        If end-game conditions are reached, displays the winner in the terminal
        and displays the user's total score on the board.
        Updates the score file with the user's name and score.
        """
        if self.draw:
            self.draw = False
            if self.comp_wins:
                print("GAME OVER\nThe computer wins this round.")
            elif self.user_wins:
                print("GAME OVER\nYou win this round.")
            elif self.tie:
                print("GAME OVER\nYou tied with the computer this round.")
            else:
                self.draw = True

        if not self.draw:  # Game has ended.
            SHIFT_FACTOR = 3
            SHIFT = self.WIDTH // SHIFT_FACTOR
            FILL_COLOR = 255 // 2
            TEXT_SIZE = 50

            message = "Your score:" + str(self.user_score)
            fill(FILL_COLOR)
            textSize(TEXT_SIZE)
            text(message, self.WIDTH // 2 - SHIFT, self.HEIGHT // 2)
            self.delay += 1

            if not self.updated_score and self.delay > 1:  # Update only once.
                self.write_score()

    def write_score(self):
        """
        Continuously prompts the user until an input of at least one character
        is given. Then updates the scores in file "othello.txt"
        """
        answer = self.input("Enter your name")
        if answer:
            scorg = ScoreOrganizer(answer, self.user_score, "othello.txt")
            scorg.update_score()
            self.updated_score = True
        else:
            print("Please enter at least one character.")

    def input(self, message=''):
        """
        Given a string message, initializes a user-interface and displays
        the message to the user. Returns user input as a string.
        """
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)
