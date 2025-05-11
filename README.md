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
This file is empty.  

*test_ai_vs_ai_simulation.py*  
This file contains the a simulate function that simulates a match between to AIs.  

*test_board.py*  
This file contains tests for Mancala board functions.  

*test_mass_ai_vs_ai_results.py*  
This file runs match mass simmulations between two AIs and stores/organizes the winners, number of moves made per game, and game durations in excel files.  

*test_match.py*  
This file contains tests Mancala Match functions.  

*test_minimax_ai.py*  
This file plays a simulated match between Minimax and VectorAI.  

*test_minimax_correctness_and_nodes.py*  
This file tests for MiniMaxAI moves for correctness.  

*test_minimax_speed.py*  
This file tests the speed of MiniMaxAI at various depth and with or without pruning.  

*test_player.py*  
This file tests for the correct assignment of player names and the amount of players created.

## Tests_outputs
*_init_.py*  

*ai_vs_ai_simulation.txt*  
This file contains the text virtualization of the match played by test_ai_vs_ai_simulation.py.  

*correct_and_node*  
This file contains the correctness and node count test results
*speed.txt*  
This contains the results of test_minimax_speed.py.  

*speed_update*  
This contains more results of test_minimax_speed.py.  

**.gitignore**  

**README.md**  
This file is this README.md

**__init__.py**  

**test_minimax_ai_temp_root.py**  
This file plays a simulated match between Minimax and VectorAI.  


