import pygame
from checkers import Game
from checkers.CONSTANTS import *

def get_row_col_from_mouse(pos):
	x, y = pos
	row = y // SQUARE_SIZE
	col = x // SQUARE_SIZE
	return row, col

def draw_screen(screen, game: Game):
	game.update(screen)
	pygame.display.update()

def main():
	pygame.init()

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Checkers')
	clock = pygame.time.Clock()


	first_play = RED

	game = Game(first_play)

	run = True
	while run:
		clock.tick(FPS)

		winner = game.board.winner()

		if winner != None:
			print(winner)

		draw_screen(screen, game)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if game.turn == first_play:
					pos = pygame.mouse.get_pos()
					row, col = get_row_col_from_mouse(pos)
					game.select(row, col)
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN and winner:
					game.reset(winner)
	
	pygame.quit()

if __name__ == '__main__':
	main()
	