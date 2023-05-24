import pygame

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // ROWS

#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
BACKGROUND = BLACK

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45, 25))