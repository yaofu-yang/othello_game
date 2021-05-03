Yao-Fu Yang

Tools Required to run code:
 - Download Processor - Python mode: https://processing.org/download/

Building/running code:
 - Open the project folder on a personal laptop (not using text editor)
 - Directly click on the 'othello_game' .pyde file to launch processor
 - Click on the play button (triangle) on the top left to launch interface.
 - To play another round, close the interface browser and re-launch by clicking the run button again.

Purpose: 
 - This project simulates a very simple othello game using international game rules.
 - The user utilizes mouse-clicks to place a legal move onto the board.
 - The user always goes first and places a black tile onto the board.
 - The computer AI always goes second and places a white tile onto the board on its turn.
 - The game continues until the board has been filled, or neither player may place a legal move.
 - Winning condition: The user has more (black) tiles on the board.
 - Losing condition: The computer has more (white) tiles on the board.
 - Tying condition: The user and computer have equal numbers of tiles on the board.
   
 Input:
  - Mouse clicks.
  - Non-legal moves will not be registered.
  
  Output:
   - If a user clicks on a legal move space during their turn, a black tile is placed.
   - The computer will place a white tile on their turn if legal moves are available.
 