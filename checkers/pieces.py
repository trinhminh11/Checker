import pygame
from .CONSTANTS import *

CROWN = pygame.transform.scale(pygame.image.load(CROWN_PATH), (45, 25))


class Piece(object):
	PADDING = 15
	BORDER = 2
	def __init__(self, row: int, col: int, color: tuple[int, int, int]):
		self.row = row
		self.col = col
		self.color = color
		self.king = False

		self.x = 0
		self.y = 0
		self.calc_pos()

	def calc_pos(self):
		self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
		self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2


	def make_king(self):
		self.king = True

	def draw(self, screen: pygame.Surface):
		radius = SQUARE_SIZE//2 - self.PADDING
		pygame.draw.circle(screen, GREY, (self.x, self.y), radius + self.BORDER)
		pygame.draw.circle(screen, self.color, (self.x, self.y), radius)

		if self.king:
			screen.blit(CROWN, (self.x - CROWN.get_width()/2, self.y - CROWN.get_height()/2))

	def move(self, row, col):
		self.row = row
		self.col = col
		self.calc_pos()
		
	def __repr__(self):
		return str(self.color)
	