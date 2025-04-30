import pygame
import math
import sys

pygame.init()
# Load custom font
PIXEL_FONT = pygame.font.Font("assets/PIXEL_FONT.ttf", 72)
PIXEL_FONT2 = pygame.font.Font("assets/PIXEL_FONT.ttf", 50)
PIXEL_FONT3 = pygame.font.Font("assets/PIXEL_FONT.ttf", 40)

# Set up window size
WIDTH, HEIGHT = 1600, 970
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mancala")

### FOR LOADING IMAGES ###
# Load background image
BG = pygame.image.load("images/spacebackground.jpeg")
# Load board image
BOARD = pygame.image.load("images/mancalaboard.png").convert_alpha()
# Load scoreboard images
ACTIVE_SCOREBOARD = pygame.image.load("images/active_player.png")
INACTIVE_SCOREBOARD = pygame.image.load("images/inactive_player.png")

### FOR RE-SIZING ###
# Re-sizes the background image
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
# Re-sizes the Mancala board image
BOARD = pygame.transform.scale(BOARD, (1536, 1024))
# Re-sizes the scoreboards
ACTIVE_SCOREBOARD = pygame.transform.scale(ACTIVE_SCOREBOARD, (400, 360))
INACTIVE_SCOREBOARD = pygame.transform.scale(INACTIVE_SCOREBOARD, (400, 360))

### FOR POSITIONING ###
# Positions the board image
board_x = (WIDTH - BOARD.get_width()) // 2 + 25
board_y = (HEIGHT - BOARD.get_height()) // 2 + 70

# Positions the stone count number for each pit
stone_count_positions = {
    # Player side; pits 0 - 5 (bottom row)
    0: (board_x + 323, board_y + 699),
    1: (board_x + 493, board_y + 699),
    2: (board_x + 656, board_y + 699),
    3: (board_x + 819, board_y + 699),
    4: (board_x + 982, board_y + 699),
    5: (board_x + 1145, board_y + 699),
    # AI side; pits 7 - 12 (top row)
    7: (board_x + 1145, board_y + 272),
    8: (board_x + 982, board_y + 272),
    9: (board_x + 819, board_y + 272),
    10: (board_x + 656, board_y + 272),
    11: (board_x + 493, board_y + 272),
    12: (board_x + 323, board_y + 272),
}

# Positions the scoreboards
player_scoreboard_pos = (1232, 750)
ai_scoreboard_pos = (-30, 50)

### FOR BUTTONS ###
# Buttons that will allow player to input which pit they would like to move their stones from on their side
pit_buttons = {
    0: {"center": (board_x + 323, board_y + 595), "radius": 65},
    1: {"center": (board_x + 487, board_y + 595), "radius": 65},
    2: {"center": (board_x + 645, board_y + 595), "radius": 65},
    3: {"center": (board_x + 805, board_y + 595), "radius": 65},
    4: {"center": (board_x + 976, board_y + 595), "radius": 65},
    5: {"center": (board_x + 1145, board_y + 595), "radius": 65},
}

### FOR GAMEPLAY VARIABLES  ###
# Initialize with four stones per pit; to be changed later with actual values
stone_count = 4
# Initialize player and AI scores to 0 for now; this represents the stone counts of each player's stores; to be changed later with actual values
player_score = 0
ai_score = 0


# Draw to screen
def draw():
    ### FOR DRAWING BACKGROUND ###
    WIN.blit(BG, (0, 0))
    WIN.blit(BOARD, (board_x, board_y))

    ### FOR DRAWING PIT STONE COUNTS ###
    for pit_index, (x, y) in stone_count_positions.items():
        # Render number of stones for corresponding pit
        text_surface = PIXEL_FONT.render(str(stone_count), True, (255, 255, 255))
        # Centers numbers within rectangle so single digit and double digit numbers are consitently centered
        text_rect = text_surface.get_rect(center=(x, y))
        # Draw text for number to the screen
        WIN.blit(text_surface, text_rect)

    ### FOR DRAWING SCOREBOARDS ###
    # Display Scoreboards
    WIN.blit(ACTIVE_SCOREBOARD, player_scoreboard_pos)
    WIN.blit(INACTIVE_SCOREBOARD, ai_scoreboard_pos)

    # Create labels for scoreboards
    player_label = PIXEL_FONT3.render("PLAYER", True, (255, 255, 255))
    ai_label = PIXEL_FONT2.render("AI", True, (255, 255, 255))

    # Draw labels onto scoreboards using scoreboard positions for reference
    WIN.blit(
        player_label, (player_scoreboard_pos[0] + 93, player_scoreboard_pos[1] + 118)
    )
    WIN.blit(ai_label, (ai_scoreboard_pos[0] + 140, ai_scoreboard_pos[1] + 110))

    # Draw the Player's score using Player scoreboard position for reference
    # Center digit text in rectangles for consistent centering for double digits
    player_score_text = PIXEL_FONT2.render(str(player_score), True, (0, 0, 0))
    player_score_rect = player_score_text.get_rect(
        center=(player_scoreboard_pos[0] + 272, player_scoreboard_pos[1] + 142)
    )
    WIN.blit(player_score_text, player_score_rect)

    # Draw AI's score using AI scoreboard position for reference
    # Center digit text in rectangles for consistent centering for double digits
    ai_score_text = PIXEL_FONT2.render(str(ai_score), True, (0, 0, 0))
    ai_score_rect = ai_score_text.get_rect(
        center=(ai_scoreboard_pos[0] + 272, ai_scoreboard_pos[1] + 142)
    )
    WIN.blit(ai_score_text, ai_score_rect)

    ### FOR DRAWING PIT BUTTONS ###
    # Draw button over each Mancala board pit
    for button in pit_buttons.values():
        pygame.draw.circle(WIN, (255, 0, 0), button["center"], button["radius"])

    pygame.display.update()


def main():
    run = True

    # Allow player to quit the game
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # Handles mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get current mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Loop through each clickable pit button
                for pit_index, button in pit_buttons.items():
                    # Horizontal distance from center
                    dx = mouse_x - button["center"][0]
                    # Vertical distance from center
                    dy = mouse_y - button["center"][1]

                    # Circle collision formula to determine if a click is inside the circle:
                    # (dx^2 + dy^2) <= radius^2
                    if dx * dx + dy * dy <= button["radius"] * button["radius"]:
                        # Insert code for processing player's move here
                        pass
        draw()

    pygame.quit()


# Game only starts when running this file directly
if __name__ == "__main__":
    main()
