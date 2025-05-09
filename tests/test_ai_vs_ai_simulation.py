
import time
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mancala.board import Board, InvalidMove
from mancala.ai_profiles import MinimaxAI, VectorAI

OUTPUT_FILE = Path("tests_outputs/ai_vs_ai_simulation.txt")

def log(message):
    print(message)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def simulate_game(ai1_class, ai2_class, depth1=4, depth2=4):
    board = Board()
    player1 = ai1_class(1, board, depth1) if ai1_class == MinimaxAI else ai1_class(1, board)
    player2 = ai2_class(2, board, depth2) if ai2_class == MinimaxAI else ai2_class(2, board)

    turn = 1
    log(f"\nNew Game: {player1.name} vs {player2.name}")
    log("Initial Board State:")
    log(board.textify_board())

    while board.legal_moves(turn):
        current_player = player1 if turn == 1 else player2
        try:
            move = current_player.get_next_move()
            if move not in board.legal_moves(turn):
                raise ValueError(f"Illegal move {move} chosen by {current_player.name}")
            log(f"Player {turn} ({current_player.name}) chooses pit {move}")
            board.board, earned_free_move = board._move_stones(turn, move)
            log(board.textify_board())
            if not earned_free_move:
                turn = 2 if turn == 1 else 1
        except Exception as e:
            log(f"Error during move: {e}")
            break

    score1, score2 = board.get_scores()
    result = f"Final Score: P1={score1}, P2={score2} — "
    if score1 > score2:
        result += f"{player1.name} Wins!"
    elif score2 > score1:
        result += f"{player2.name} Wins!"
    else:
        result += "Draw!"
    log(result)

def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("AI vs AI Match Simulation Log\n")

    simulate_game(MinimaxAI, VectorAI, depth1=4)
    simulate_game(MinimaxAI, MinimaxAI, depth1=4, depth2=6)
    simulate_game(VectorAI, VectorAI)

if __name__ == "__main__":
    main()
