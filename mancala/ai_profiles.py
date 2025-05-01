""" Module for Mancala AI Profiles. """

import copy
from random import choice

from mancala.mancala import Player, reverse_index
from mancala.constants import AI_NAME, P1_PITS, P2_PITS
from mancala.board import InvalidMove

class AIPlayer(Player):
    """ Base class for an AI Player """
    def __init__(self, number, board, name=AI_NAME):
        """ Initializes an AI profile. """
        super(AIPlayer, self).__init__(number, board, name)
        self.name = "VectorAI"

    @property
    def pits(self):
        """ Shortcut to AI pits. """
        if self.number == 1:
            return self.board.board[P1_PITS]
        else:
            return self.board.board[P2_PITS]

    @property
    def eligible_moves(self):
        """ Returns a list of integers representing eligible moves. """
        eligible_moves = []
        for i in range(len(self.pits)):
            if not self.pits[i] == 0:
                eligible_moves.append(i)
        return eligible_moves

    @property
    def eligible_free_turns(self):
        """ Returns a list of indexes representing eligible free turns. """

        free_turn_indices = range(6, 0, -1)

        elig_free_turns = []

        for i in range(0, 6):
            if self.pits[i] == free_turn_indices[i]:
                elig_free_turns.append(1)
            else:
                elig_free_turns.append(0)

        return elig_free_turns

    def _think(self):
        """ Slight delay for thinking. """
        import time
        print("AI is thinking...")
        time.sleep(3)

class RandomAI(AIPlayer):
    """ AI Profile that randomly selects from eligible moves. """

    def get_next_move(self):
        """ Returns next AI move based on profile. """

        self._think()

        return choice(self.eligible_moves)

class VectorAI(AIPlayer):
    """ AI Profile using a simple vector decision method. """

    def get_next_move(self):
        """ Use an reverse indices vector to optimize for free turns. """

        self._think()

        reverse_indices = range(5, -1, -1)

        # First optimize for free moves.
        for i in reverse_indices:
            if self.eligible_free_turns[i] == 1:
                if self.pits[i] == reverse_index(i) + 1:
                    print("VectorAI, mode 1, playing: ", str(i))
                    return i
        # Then clear out inefficient pits.
        for i in reverse_indices:
            if self.pits[i] > reverse_index(i) + 1:
                print("VectorAI, mode 2, playing: ", str(i))
                return i
        # Finally, select a random eligible move.
        print("VectorAI, mode 3, playing an eligible move.")
        return choice(self.eligible_moves)

# Old Eval Function (simple store score comparison only)
# def evaluate_board(board, player_num):
#     score1, score2 = board.get_scores()
#     return score1 - score2 if player_num == 1 else score2 - score1

# New Evaluation Function:
# Adds pit control to scoring and gives higher weight to store points (captures)
def evaluate_board(board, player_num):
    score1, score2 = board.get_scores()

    # Sum of stones on each player's side (not store)
    side1 = sum(board.board[0])  # Player 1's pits (top row)
    side2 = sum(board.board[2])  # Player 2's pits (bottom row)

    # Calculate score differences from perspective of current player
    if player_num == 1:
        store_score = score1 - score2       # Difference in captured/store stones
        side_score = side1 - side2          # Difference in stones still on the board
    else:
        store_score = score2 - score1
        side_score = side2 - side1

    # Combine weighted components: prioritize captures over control
    return (4 * store_score) + (1 * side_score)


# Core Minimax Algorithm:
# Recursively simulate future moves up to 'depth', evaluating the best move for the current player.
def minimax(board, depth, maximizing_player, player_num):
    # Base case: depth limit reached, return evaluation of current board
    if depth == 0:
        return evaluate_board(board, player_num), None

    # Determine which player's turn it is (alternate each level)
    current_player = player_num if maximizing_player else 3 - player_num
    legal_moves = board.legal_moves(current_player)

    # If no legal moves, evaluate board as-is
    if not legal_moves:
        return evaluate_board(board, player_num), None

    best_move = None

    if maximizing_player:
        # Maximize score for current player
        max_eval = float('-inf')
        for move in legal_moves:
            new_board = copy.deepcopy(board)  # Simulate new board state
            try:
                new_board.board, _ = new_board._move_stones(current_player, move)
            except InvalidMove:
                continue
            eval_score, _ = minimax(new_board, depth - 1, False, player_num)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        # Minimize opponent’s score
        min_eval = float('inf')
        for move in legal_moves:
            new_board = copy.deepcopy(board)
            try:
                new_board.board, _ = new_board._move_stones(current_player, move)
            except InvalidMove:
                continue
            eval_score, _ = minimax(new_board, depth - 1, True, player_num)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


# MinimaxAI wrapper:
# Uses the minimax algorithm to determine and return the best next move.
class MinimaxAI:
    def __init__(self, number, board, depth=4):
        self.number = number
        self.board = board
        self.depth = depth
        self.name = f"Minimax(depth={depth})"

    def get_next_move(self):
        # Start the minimax search assuming it's the maximizing player's turn
        _, move = minimax(self.board, self.depth, True, self.number)
        return move

