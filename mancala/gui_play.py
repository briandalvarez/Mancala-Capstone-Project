import pygame
import sys

pygame.init()

# Set up window size
WIDTH, HEIGHT = 1600, 950
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mancala")

# Load background image
BG = pygame.image.load("spacebackground.jpeg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# Load board image
BOARD = pygame.image.load("mancalaboard.png").convert_alpha()
BOARD = pygame.transform.scale(BOARD, (1536, 1024))

# Position board image
board_x = (WIDTH - BOARD.get_width()) // 2
board_y = (HEIGHT - BOARD.get_height()) // 2 + 50


# Display background image to the screen
def draw():
    WIN.blit(BG, (0, 0))
    WIN.blit(BOARD, (board_x, board_y))
    pygame.display.update()


def main():
    run = True

    # Allow player to quit the game
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw()

    pygame.quit()


# Game only starts when running this file directly
if __name__ == "__main__":
    main()
