import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mancala.board import Board
from mancala.ai_profiles import MinimaxAI, eval_counter

OUTPUT_FILE = "tests_outputs/correct_and_node"

def log(message):
    print(message)
    with open(OUTPUT_FILE, "a") as f:
        f.write(message + "\n")

def test_move_correctness():
    # Define a test board state where the best move is known
    test_state = [
        [0, 0, 0, 0, 1, 0],  # Player 1 pits
        [20],               # Player 1 store
        [4, 4, 4, 4, 4, 4],  # Player 2 pits
        [10],               # Player 2 store
    ]
    board = Board(test_state=test_state)
    ai = MinimaxAI(number=2, board=board, depth=4)
    move = ai.get_next_move()
    log(f"Correctness Test - Selected move: {move}")
    expected = 0  # Assuming best move is pit 0 in this setup
    assert move == expected, f"Expected move {expected}, got {move}"

def log_node_counts_by_depth():
    log("\n=== Node Count by Depth (Pruned) ===")
    test_state = [
        [12, 12, 12, 12, 12, 12],
        [0],
        [12, 12, 12, 12, 12, 12],
        [0],
    ]
    for depth in [2, 4, 6, 8]:
        ai = MinimaxAI(number=2, board=Board(test_state=test_state), depth=depth)
        start = time.time()
        ai.get_next_move()
        end = time.time()
        log(f"Depth {depth}: {eval_counter['count']} evaluations in {end - start:.2f} sec")
        eval_counter['count'] = 0

def main():
    with open(OUTPUT_FILE, "w") as f:
        f.write("Correctness and Node Count Test Results\n")
    test_move_correctness()
    log_node_counts_by_depth()

if __name__ == "__main__":
    main()
