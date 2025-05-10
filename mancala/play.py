""" Main script to begin playing a match of Mancala. """
from mancala.mancala import Match, HumanPlayer
from mancala.ai_profiles import VectorAI, MinimaxAI

def main():
    """ Script to begin a match of Mancala. """
    print("Welcome to Mancala!")
    # Uncomment to - Play against the VectorAI (Original Implementation)
    # match = Match(player1_type=HumanPlayer, player2_type=VectorAI)

    # Play against the MinMaxAI (Human vs. MinMaxAI)
    match = Match(player1_type=HumanPlayer, player2_type=lambda n, b: MinimaxAI(n, b, depth=4))

    match.handle_next_move()

if __name__ == '__main__':
    main()
