from mancala.board import Board
from mancala.ai_profiles import MinimaxAI, VectorAI
from mancala.constants import P1_PITS, P2_PITS

def simulate_game(player1, player2, depth=4):
    # Initialize game state and both players
    board = Board(gui=None)
    p1 = player1(1, board) if callable(player1) else player1
    p2 = player2(2, board) if callable(player2) else player2

    # Start with player 1 (Minimax)
    current_player = p1
    # Keep track of all moves made
    move_log = []
    # Count how many turns have occurred
    turns = 0

    # Continue playing until either side of the board is empty
    while set(board.board[P1_PITS]) != {0} and set(board.board[P2_PITS]) != {0}:
        if turns > 200:
            print("Too many turns — possible infinite loop. Exiting.")
            break  # Safety net to avoid infinite loops

        legal = board.legal_moves(current_player.number)
        print(f"\nTurn {turns + 1}: {current_player.name}'s turn. Legal moves: {legal}")

        if not legal:
            print(f"No legal moves for {current_player.name}. Ending game.")
            break

        move = current_player.get_next_move()  # Let AI choose a move
        print(f"{current_player.name} selects move: {move}")
        move_log.append((current_player.name, move))

        # Apply the move to the board and check if it earned a free turn
        board.board, board.free_turn_earned = board._move_stones(current_player.number, move)

        # If no free turn, switch players
        if not board.free_turn_earned:
            current_player = p1 if current_player == p2 else p2

        turns += 1

    # Get final scores from the board
    score1, score2 = board.get_scores()
    print("\nFinal Score: MinmaxAI = {}, VectorAI = {}".format(score1, score2))

    # Determine the winner
    if score1 > score2:
        winner = "MinimaxAI"
    elif score2 > score1:
        winner = "VectorAI"
    else:
        winner = "Tie"
    print("Winner:", winner)

    # Display move history in a nicely formatted list
    print("\nMove Log:")
    for i, (player, move) in enumerate(move_log, start=1):
        print(f"{i:>3}. {player:<16} → pit {move}")


# Run a single match between Minimax and VectorAI
if __name__ == "__main__":
    simulate_game(
        lambda n, b: MinimaxAI(None, n, b, depth=6),  # Player 1: MinimaxAI with depth 6
        lambda n, b: VectorAI(None, n, b)             # Player 2: VectorAI
    )
