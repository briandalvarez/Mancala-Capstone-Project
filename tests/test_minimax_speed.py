
import time
import copy
import hashlib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mancala.board import Board
from mancala.ai_profiles import MinimaxAI, eval_counter, evaluate_board

OUTPUT_FILE = "tests_outputs/speed_update"

def board_hash(board):
    # Create a hash of the board state for before/after comparison
    flat = sum(board.board, [])
    return hashlib.md5(str(flat).encode()).hexdigest()

def log(message):
    print(message)
    with open(OUTPUT_FILE, "a") as f:
        f.write(message + "\n")

def run_minimax_test(depth, test_state=None, disable_pruning=False):
    log(f"\n=== Running MinimaxAI at depth {depth} ===")

    if test_state:
        board = Board(test_state=copy.deepcopy(test_state))
    else:
        board = Board()

    # Save original board state hash
    before_hash = board_hash(board)

    # Optionally disable pruning by monkey-patching minimax
    if disable_pruning:
        from mancala.ai_profiles import minimax as original_minimax

        def unpruned_minimax(board, depth, maximizing_player, player_num, alpha=float('-inf'), beta=float('inf')):
            if depth == 0:
                return evaluate_board(board, player_num), None
            current_player = player_num if maximizing_player else 3 - player_num
            legal_moves = board.legal_moves(current_player)
            if not legal_moves:
                return evaluate_board(board, player_num), None
            best_move = None
            if maximizing_player:
                max_eval = float("-inf")
                for move in legal_moves:
                    new_board = board.clone(include_gui=False)
                    try:
                        new_board.board, _ = new_board._move_stones(current_player, move)
                    except:
                        continue
                    eval_score, _ = unpruned_minimax(new_board, depth - 1, False, player_num, alpha, beta)
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = move
                    alpha = max(alpha, eval_score)
                return max_eval, best_move
            else:
                min_eval = float("inf")
                for move in legal_moves:
                    new_board = board.clone(include_gui=False)
                    try:
                        new_board.board, _ = new_board._move_stones(current_player, move)
                    except:
                        continue
                    eval_score, _ = unpruned_minimax(new_board, depth - 1, True, player_num, alpha, beta)
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = move
                    beta = min(beta, eval_score)
                return min_eval, best_move

        from mancala import ai_profiles
        ai_profiles.minimax = unpruned_minimax

    ai = MinimaxAI(number=2, board=board, depth=depth)

    start_time = time.time()
    move = ai.get_next_move()
    end_time = time.time()

    after_hash = board_hash(board)
    mutated = before_hash != after_hash

    elapsed = end_time - start_time

    log(f"Depth {depth} completed. Chosen move: {move}")
    log(f"Time taken: {elapsed:.4f} seconds")
    log(f"Evaluated board states: {eval_counter['count']}")
    log(f"Board mutated: {'YES' if mutated else 'NO'}")
    eval_counter['count'] = 0

def main():
    with open(OUTPUT_FILE, "w") as f:
        f.write("Mancala MinimaxAI Deep Correctness Benchmark\n")

    deep_state = [
        [12, 12, 12, 12, 12, 12],
        [0],
        [12, 12, 12, 12, 12, 12],
        [0],
    ]

    for depth in [2, 4, 6, 8, 10]:
        run_minimax_test(depth, test_state=deep_state, disable_pruning=False)

    log("\n=== Now running without pruning ===")
    for depth in [2, 4]:
        run_minimax_test(depth, test_state=deep_state, disable_pruning=True)

if __name__ == "__main__":
    main()
