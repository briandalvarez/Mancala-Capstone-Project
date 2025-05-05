"""Mancala app."""

from mancala.constants import DEFAULT_NAME, P1_PITS, P2_PITS, P1_STORE, P2_STORE
from mancala.board import Board, InvalidMove
import time

#For testing purposes only!!!
import random


class Player(object):
    """A player of Mancala."""

    def __init__(self, gui, number=None, board=None, name=DEFAULT_NAME):
        self.name = name
        self.number = number
        self.board = board
        self.gameGUI = gui

    def __str__(self):
        return "Player: %s" % self.name

    def get_name(self):
        """Returns player name."""
        return self.name


class Match(object):
    """A match of Mancala has two Players and a Board.

    Match tracks current turn.

    """

    def __init__(self, gui, player1_type=Player, player2_type=Player):
        """Initializes a new match."""
        self.gameGUI = gui
        self.board = Board(self.gameGUI)
        self.players = [player1_type(self.gameGUI, 1, self.board), player2_type(self.gameGUI, 2, self.board)]
        self.player1 = self.players[0] #Player1 must always be human
        self.player2 = self.players[1]  #Player2 must always be AI
        self.current_turn = self.player1

    def handle_next_move(self, move=0):
        """Shows board and handles next move."""
        #self.board.textify_board()
        self.gameGUI.update_scoreboard(self.board.board_array())

        # Human logic
        if self.current_turn == self.player1:
            # Prevent invalid move (clicking on an empty pit)
            if self.board.board[0][move] == 0:
                if self.gameGUI:
                    self.gameGUI.update_display("That pit is empty. Try another one.")
                return

            next_move = move
            print(f"Human move was {next_move}")
            if self.gameGUI:
                self.gameGUI.update_display("Please select your next move (1 to 6)!")

        # AI logic
        # Ensures AI never tries to play an empty pit. Prevents crashing due to invalid moves.
        elif self.current_turn == self.player2:  # AI
            while True:
                next_move = self.current_turn.get_next_move()
                if self.board.board[2][next_move] > 0:
                    break  # Valid move
                else:
                    print(f"AI selected empty pit {next_move}. Retrying...")
            print(f"AI move was {next_move}")

            # Sanity check: Ensure AI's move is not from an empty pit
            if self.board.board[2][next_move] == 0:
                if self.gameGUI:
                    self.gameGUI.update_display("AI attempted an invalid move. Skipping.")
                return  # Or handle with fail-safe logic if needed
        free_move_earned = False  # Always initialize this to prevent UnboundLocalError

        try:
            self.board.board, free_move_earned = self.board._move_stones(
                self.current_turn.number, next_move
            )
        except InvalidMove:
            # Check whether game was won by AI.
            if self._check_for_winner():
                import sys

                sys.exit()
            if isinstance(self.current_turn, HumanPlayer):
                if self.gameGUI:
                    self.gameGUI.update_display("Invalid move. Please choose a pit with stones.")
            # Early return to avoid duplicate recursive execution
            return


        # Check whether game was won.
        if self._check_for_winner():
            import sys

            sys.exit()

        # Check whether free move was earned
        if free_move_earned:
            if self.current_turn == self.player1: # Human
                return
            elif self.current_turn == self.player2: # AI
                self.handle_next_move()
        else:
            if self.current_turn == self.player1: # Human
                self.gameGUI.isButtonsActvive = False
                self.gameGUI.update_buttons()
                self._swap_current_turn()
                self.handle_next_move()
            elif self.current_turn == self.player2: # AI
                self.gameGUI.isButtonsActvive = True
                self._swap_current_turn()
                return
                

    def _swap_current_turn(self):
        """Swaps current turn to the other player."""
        if self.current_turn == self.player1:
            self.current_turn = self.player2
            print("It is now AI's turn!")
            return self.player2
        else:
            self.current_turn = self.player1
            print("It is now the Human's turn!")
            return self.player1

    def _check_for_winner(self):
        """Checks for winner. Announces the win."""
        if set(self.board.board[P1_PITS]) == set([0]):
            self.board.board = self.board.gather_remaining(self.player2.number)
            '''print(
                "Player 1 finished! %s: %d to %s: %d"
                % (
                    self.player1.name,
                    self.board.board[P1_STORE][0],
                    self.player2.name,
                    self.board.board[P2_STORE][0],
                )
            )'''
            #Displays in GUI
            self.gameGUI.update_display("Player 2 finished! %s: %d to %s: %d"
            % (
                self.player1.name,
                self.board.board[P1_STORE][0],
                self.player2.name,
                self.board.board[P2_STORE][0],
            ))
            return True
        elif set(self.board.board[P2_PITS]) == set([0]):
            self.board.board = self.board.gather_remaining(self.player1.number)
            '''print(
                "Player 2 finished! %s: %d to %s: %d"
                % (
                    self.player1.name,
                    self.board.board[P1_STORE][0],
                    self.player2.name,
                    self.board.board[P2_STORE][0],
                )
            )'''
            #Displays in GUI
            self.gameGUI.update_display("Player 2 finished! %s: %d to %s: %d"
                % (
                    self.player1.name,
                    self.board.board[P1_STORE][0],
                    self.player2.name,
                    self.board.board[P2_STORE][0],
                ))
            return True
        else:
            return False


class HumanPlayer(Player):
    """A human player."""

    def __init__(self, gui, number, board, name=None):
        super(HumanPlayer, self).__init__(gui, number, board)
        if name:
            self.name = name
        else:
            self.name = self.get_human_name()

    def get_human_name(self):
        """Gets inputted player name from GUI"""
        return self.gameGUI.get_playername()

    '''def get_next_move(self):
        """Gets next move from a human player."""
        #Display prompt
        self.gameGUI.set_display_text("Please select your next move (1 to 6)!")
        #value = int(input("Please input your next move (1 to 6): "))
        value = random.randint(1, 6)
        return value - 1'''


def reverse_index(index):
    """Returns the mirror index to the one given."""
    rev_index = range(5, -1, -1)
    return rev_index[index]
