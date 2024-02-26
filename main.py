import pygame
from checkers import Game
from checkers.CONSTANTS import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
clock = pygame.time.Clock()

def get_row_col_from_mouse(pos):
	x, y = pos
	row = y // SQUARE_SIZE
	col = x // SQUARE_SIZE
	return row, col

def draw_screen(screen, game):
	game.update(screen)

	pygame.display.update()


def main():
	game = Game()

	run = True
	while run:
		clock.tick(FPS)
		if game.board.winner()!= None:
			print(game.board.winner())
		draw_screen(screen, game)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				row, col = get_row_col_from_mouse(pos)
				game.select(row, col)
				
	
	pygame.quit()

if __name__ == '__main__':
	main()