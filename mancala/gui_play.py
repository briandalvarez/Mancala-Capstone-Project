import pygame
import math
import sys
from mancala.mancala import Match, HumanPlayer
from mancala.ai_profiles import VectorAI, MinimaxAI

class GUI():
    def __init__(self):

        pygame.init()
        # Load custom font
        self.PIXEL_FONT = pygame.font.Font("assets/PIXEL_FONT.ttf", 72)
        self.PIXEL_FONT2 = pygame.font.Font("assets/PIXEL_FONT.ttf", 50)
        self.PIXEL_FONT3 = pygame.font.Font("assets/PIXEL_FONT.ttf", 40)
        self.PIXEL_FONT4 = pygame.font.Font("assets/PIXEL_FONT.ttf", 100)

        # Set up window size
        self.WIDTH, self.HEIGHT = 1600, 970
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Mancala")

        ### FOR LOADING IMAGES ###
        # Load background image
        self.BG = pygame.image.load("images/spacebackground.jpeg")
        # Load board image
        self.BOARD = pygame.image.load("images/mancalaboard.png").convert_alpha()
        # Load scoreboard images
        self.ACTIVE_SCOREBOARD = pygame.image.load("images/active_player.png")
        self.INACTIVE_SCOREBOARD = pygame.image.load("images/inactive_player.png")

        ### FOR RE-SIZING ###
        # Re-sizes the background image
        self.BG = pygame.transform.scale(self.BG, (self.WIDTH, self.HEIGHT))
        # Re-sizes the Mancala board image
        self.BOARD = pygame.transform.scale(self.BOARD, (1536, 1024))
        # Re-sizes the scoreboards
        self.ACTIVE_SCOREBOARD = pygame.transform.scale(self.ACTIVE_SCOREBOARD, (400, 360))
        self.INACTIVE_SCOREBOARD = pygame.transform.scale(self.INACTIVE_SCOREBOARD, (400, 360))

        ### FOR POSITIONING ###
        # Positions the board image
        self.board_x = (self.WIDTH - self.BOARD.get_width()) // 2 + 25
        self.board_y = (self.HEIGHT - self.BOARD.get_height()) // 2 + 70

        # Positions the stone count number for each pit
        self.stone_count_positions = {
            # Player side; pits 0 - 5 (bottom row)
            0: (self.board_x + 323, self.board_y + 699),
            1: (self.board_x + 493, self.board_y + 699),
            2: (self.board_x + 656, self.board_y + 699),
            3: (self.board_x + 819, self.board_y + 699),
            4: (self.board_x + 982, self.board_y + 699),
            5: (self.board_x + 1145, self.board_y + 699),
            # AI side; pits 7 - 12 (top row)
            7: (self.board_x + 1145, self.board_y + 272),
            8: (self.board_x + 982, self.board_y + 272),
            9: (self.board_x + 819, self.board_y + 272),
            10: (self.board_x + 656, self.board_y + 272),
            11: (self.board_x + 493, self.board_y + 272),
            12: (self.board_x + 323, self.board_y + 272),
        }

        # Positions the scoreboards
        self.player_scoreboard_pos = (1232, 750)
        self.ai_scoreboard_pos = (-30, 50)

        ### FOR BUTTONS ###
        # Buttons that will allow player to input which pit they would like to move their stones from on their side
        self.pit_buttons = {
            0: {"center": (self.board_x + 323, self.board_y + 595), "radius": 65},
            1: {"center": (self.board_x + 487, self.board_y + 595), "radius": 65},
            2: {"center": (self.board_x + 645, self.board_y + 595), "radius": 65},
            3: {"center": (self.board_x + 805, self.board_y + 595), "radius": 65},
            4: {"center": (self.board_x + 976, self.board_y + 595), "radius": 65},
            5: {"center": (self.board_x + 1145, self.board_y + 595), "radius": 65},
        }


        ### FOR GAMEPLAY VARIABLES  ###
        # Initialize with four stones per pit; to be changed later with actual values
        self.stone_count = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        # Initialize player and AI scores to 0 for now; this represents the stone counts of each player's stores; to be changed later with actual values
        self.player_score = self.stone_count[6]
        self.ai_score = self.stone_count[13]

        ###Input Box Variables and enter button
        self.active_color =  (102, 178, 255)
        self.inactive_color =  (0, 102, 204)
        self.current_color = self.inactive_color
        self.input_box = pygame.Rect(810, 305, 500, 60)
        self.input_box_text = ''

        self.enter_button = pygame.Rect(690, 395, 200, 100)

        #Making player name a variable
        self.player_name = 'Player'

        #Display box and text
        self.display_box = pygame.Rect(345, 40, 1200, 200)
        self.display_text = ''

        #Handling pit buttons
        self.isButtonsActvive = True


    def update_buttons(self):
        self.draw_pit_stone_counts()
        pygame.display.update()

    def set_display_text(self, text):
        self.display_text = text

    def set_playername(self):
        self.player_name = self.input_box_text

    def get_playername(self):
        return self.player_name

    def update_display(self, text):
        self.display_text = text

        #Draw Display Box
        pygame.draw.rect(self.WIN, (0, 0, 137), self.display_box)
        pygame.draw.rect(self.WIN, (255, 255, 255), self.display_box, 10)

        #Draw Display text
        displayed_text = self.PIXEL_FONT2.render(self.display_text, True, (255, 255, 255))
        self.WIN.blit(displayed_text, (380, 105))

        pygame.display.update()

    def draw_game_screen(self):
        ### FOR DRAWING BACKGROUND ###
        self.WIN.blit(self.BG, (0, 0))
        self.WIN.blit(self.BOARD, (self.board_x, self.board_y))

        ### FOR DRAWING SCOREBOARDS ###
        # Display Scoreboards
        self.WIN.blit(self.ACTIVE_SCOREBOARD, self.player_scoreboard_pos)
        self.WIN.blit(self.INACTIVE_SCOREBOARD, self.ai_scoreboard_pos)

        # Create labels for scoreboards
        player_label = self.PIXEL_FONT3.render(self.player_name, True, (255, 255, 255))
        ai_label = self.PIXEL_FONT2.render("AI", True, (255, 255, 255))

        # Draw labels onto scoreboards using scoreboard positions for reference
        self.WIN.blit(player_label, (self.player_scoreboard_pos[0] + 93, self.player_scoreboard_pos[1] + 118))
        self.WIN.blit(ai_label, (self.ai_scoreboard_pos[0] + 140, self.ai_scoreboard_pos[1] + 110))

        #Draw Display Box
        pygame.draw.rect(self.WIN, (0, 0, 137), self.display_box)
        pygame.draw.rect(self.WIN, (255, 255, 255), self.display_box, 10)

        #Draw Display text
        displayed_text = self.PIXEL_FONT2.render(self.display_text, True, (255, 255, 255))
        self.WIN.blit(displayed_text, (380, 105))

        #Draw everthing else
        self.draw_pit_stone_counts()
        self.draw_scores()
        self.draw_buttons()

        #pygame.display.update()

    def draw_pit_stone_counts(self):
        for pit_index, (x, y) in self.stone_count_positions.items():
            # Render number of stones for corresponding pit
            text_surface = self.PIXEL_FONT.render(str(self.stone_count[pit_index]), True, (255, 255, 255))
            # Centers numbers within rectangle so single digit and double digit numbers are consitently centered
            text_rect = text_surface.get_rect(center=(x, y))
            # Draw text for number to the screen
            self.WIN.blit(text_surface, text_rect)

            #pygame.display.update()

    def draw_scores(self):
        # Draw the Player's score using Player scoreboard position for reference
        # Center digit text in rectangles for consistent centering for double digits
        player_score_text = self.PIXEL_FONT2.render(str(self.player_score), True, (0, 0, 0))
        player_score_rect = player_score_text.get_rect(
            center=(self.player_scoreboard_pos[0] + 272, self.player_scoreboard_pos[1] + 142)
        )
        self.WIN.blit(player_score_text, player_score_rect)

        # Draw AI's score using AI scoreboard position for reference
        # Center digit text in rectangles for consistent centering for double digits
        ai_score_text = self.PIXEL_FONT2.render(str(self.ai_score), True, (0, 0, 0))
        ai_score_rect = ai_score_text.get_rect(
            center=(self.ai_scoreboard_pos[0] + 272, self.ai_scoreboard_pos[1] + 142)
        )
        self.WIN.blit(ai_score_text, ai_score_rect)
        #pygame.display.update()

    def draw_buttons(self):
        ### FOR DRAWING PIT BUTTONS ###
        # Draw button over each Mancala board pit
        if self.isButtonsActvive == False:
            for button in self.pit_buttons.values():
                pygame.draw.circle(self.WIN, (0, 0, 137), button["center"], button["radius"])
        elif self.isButtonsActvive == True:
            for button in self.pit_buttons.values():
                pygame.draw.circle(self.WIN, (204, 85, 0), button["center"], button["radius"])

        #pygame.display.update()

    def update_scoreboard(self, newScores):
        self.stone_count = newScores[:]
        self.player_score = self.stone_count[6]
        self.ai_score = self.stone_count[13]
        self.draw_game_screen()
        pygame.display.update()



    def draw_welcome_screen(self):
        self.WIN.fill((0, 0, 137))
        welcome_text = self.PIXEL_FONT4.render("Welcome to Mancala!", True, (255, 255, 255))
        self.WIN.blit(welcome_text, (280, 180))

        #Draw input box label
        input_label = self.PIXEL_FONT2.render("Please input your name: ", True, (255, 255, 255))
        self.WIN.blit(input_label, (240, 300))

        #Draw input box
        pygame.draw.rect(self.WIN, self.current_color, self.input_box)

        #Draw inputted text
        input_text = self.PIXEL_FONT2.render(self.input_box_text, True, (255, 255, 255))
        self.WIN.blit(input_text, (830, 305))

        #Draw enter button
        pygame.draw.rect(self.WIN, (204, 85, 0), self.enter_button)
        pygame.draw.rect(self.WIN, (153, 51, 0), self.enter_button, 10)

        #Draw button label
        enter_button_label = self.PIXEL_FONT2.render("Enter", True, (153, 51, 0))
        self.WIN.blit(enter_button_label, (720, 410))

        #pygame.display.update()



def main():
    run = True
    #Game States (welcome, game, gameover)
    game_state = 'welcome'
    #Initalize GUI (class)
    GameGUI = GUI()
    is_input_box_active = False


    #match = match = Match(player1_type=HumanPlayer, player2_type=VectorAI)

    # Allow player to quit the game
    while run:
        #match.handle_next_move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # Draw based on state
            if game_state == 'welcome':
                GameGUI.draw_welcome_screen()

                # Click inside the input box to activate
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if GameGUI.input_box.collidepoint(event.pos):
                        is_input_box_active = True
                        GameGUI.current_color = GameGUI.active_color
                    else:
                        active = False
                        color = GameGUI.inactive_color
                        is_input_box_active = False
                        GameGUI.current_color = GameGUI.inactive_color

                if event.type == pygame.KEYDOWN:
                    if is_input_box_active:
                        if event.key == pygame.K_BACKSPACE:
                            GameGUI.input_box_text = GameGUI.input_box_text[:-1]
                        else:
                            GameGUI.input_box_text += event.unicode

                #Click Enter button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if GameGUI.enter_button.collidepoint(event.pos):
                        GameGUI.set_playername()
                        game_state = 'game'
                        match = Match(GameGUI, HumanPlayer, MinimaxAI)
                        #match = Match(GameGUI, HumanPlayer, VectorAI)
                        #match.handle_next_move()
                    

            elif game_state == 'game':
                GameGUI.draw_game_screen()

                if GameGUI.isButtonsActvive == True:
                    GameGUI.update_display("Please select your next move (1 to 6)!")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get current mouse position
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        # Loop through each clickable pit button
                        for pit_index, button in GameGUI.pit_buttons.items():
                            # Horizontal distance from center
                            dx = mouse_x - button["center"][0]
                            # Vertical distance from center
                            dy = mouse_y - button["center"][1]

                            # Circle collision formula to determine if a click is inside the circle:
                            # (dx^2 + dy^2) <= radius^2
                            if dx * dx + dy * dy <= button["radius"] * button["radius"]:
                                # Insert code for processing player's move here
                                #print(pit_index)
                                match.handle_next_move(pit_index)
                                print("Handle_next_move triggered by GUI human click")
                #match.handle_next_move()

            pygame.display.flip()
            

        

    pygame.quit()


# Game only starts when running this file directly
if __name__ == "__main__":
    main()
