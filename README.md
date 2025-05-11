# Mancala-Capstone-Project
CPSC 481 capstone: AI agent vs human opponent Mancala game with GUI

## Assets  
*PIXEL_FONT.ttf*  
This file contains the font used in our GUI.

## Images
*active_player.png*  
*green_star.png*  
*inactive_player.png*  
*mancalaboard.png*  
*pink_star.png*  
*purple_star.png*  
*spacebackground.jpeg*  
*yellow_star.png*  

This folder contains the image files used in the background of our GUI game screen and the image used for the mancala board.

## Mancala  
*__init__.py*  

*ai_profiles.py*  
This file contains the previously existing AI players VectorAI and RandomAI(as well as the supporting class of AIPlayer), as well as our evaluation function, minimax algorithm, and MiniMaxAI class.  

*board.py*  
This file contains the previously existing board class that handles all board changes and board logic.  

*constants.py*  
This files contains constant variables that are used throughout the project.  

*gui_play.py*  
This file contains our GUI and gameGUI class.This is the file that our projects main file(from where our program is run), and is run with the **python -m mancala.gui_play** command.  

*mancala.py*  
This file contains the previously existing match class that contains the game playthrough logic, as well as the Player class which acts as a parent class to the HumanPlayer, VectorAI and RandomAI classes.  

*play.py*  
This file was the main file of the original repository(where the project was run from).

## Tests  
*_init_.py*  
*test_ai.py*  
*test_ai_vs_ai_simulation.py*  
*test_board.py*  
*test_match.py*  
*test_minimax_ai.py*  
*test_minimax_correctness_and_nodes.py*  
*test_minimax_speed.py*  
*test_player.py*

## Tests_outputs
*_init_.py*  
*ai_vs_ai_simulation.txt*  
*correct_and_node*  
*speed.txt*  
*speed_update*

**.gitignore**  

**README.md**  

**__init__.py**  

**test_minimax_ai_temp_root.py**  

