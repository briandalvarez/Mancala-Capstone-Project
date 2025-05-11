import time
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
#Excel library
import pandas as pd
#python3 -m venv myenv
#source myenv/bin/activate
#pip install pandas openpyxl
#To exit: deactivate


from mancala.board import Board, InvalidMove
from mancala.ai_profiles import MinimaxAI, VectorAI, RandomAI


def simulate_game(ai1_class, ai2_class, depth1=4, depth2=4):
    board = Board()
    player1 = ai1_class(1, board, depth1) if ai1_class == MinimaxAI else ai1_class(1, board)
    player2 = ai2_class(2, board, depth2) if ai2_class == MinimaxAI else ai2_class(2, board)

    turn = 1
    moveCount = 0
    
    #Mark start time
    startTime = time.perf_counter()

    while board.legal_moves(turn):
        current_player = player1 if turn == 1 else player2
        try:
            move = current_player.get_next_move()
            if move not in board.legal_moves(turn):
                raise ValueError(f"Illegal move {move} chosen by {current_player.name}")
            #Keep track of total number of moves made in game
            moveCount += 1
            board.board, earned_free_move = board._move_stones(turn, move)
            if not earned_free_move:
                turn = 2 if turn == 1 else 1
        except Exception as e:
            print(f"Error during move: {e}")
            break

    score1, score2 = board.get_scores()
    if score1 > score2:
        winner = player1.name + "1"
    elif score2 > score1:
        winner = player2.name + "2"
    else:
        winner = "Draw"

    #Clock end time
    endTime = time.perf_counter()
    gameDuration = round((endTime - startTime), 4)
    print(winner)
    print(moveCount)
    print(gameDuration)

    return winner, moveCount, gameDuration

def main():
    
    #Getting test details from user
    print("Simulation Options:")
    print("1. VectorAI vs RandomAI")
    print("2. MiniMaxAI vs RamdomAI")
    print("3. VectorAI vs MiniMaxAI")
    print("4. RandomAI vs RandomAI")
    sim = int(input("Select the simulation to run(1-3): "))
    fileName = input("Provide a file name to save the test results: ")
    matchNum = int(input("How many simulations would you like to perform: "))
    fileName += ".xlsx"

    #Results stored in
    results = []
    winner = ""
    moves = 0
    time = 0.0

    for i in range(matchNum):
        if(sim == 1):
            winner, moves, time = simulate_game(VectorAI, RandomAI)
        elif(sim == 2):
            winner, moves, time = simulate_game(MinimaxAI, RandomAI, depth1=4)
        elif(sim == 3):
            winner, moves, time = simulate_game(MinimaxAI, VectorAI, depth1=4)
        elif(sim == 4):
            winner, moves, time = simulate_game(RandomAI, RandomAI)
        results.append({
        "Winner": winner,
        "Total # of moves made": moves,
        "Total Game Time(seconds)": time
    })

    #print(results)
    df = pd.DataFrame(results)
    df.to_excel(fileName, index=False)


if __name__ == "__main__":
    main()
