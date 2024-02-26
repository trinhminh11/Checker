import pygame
from .board import Board
from .CONSTANTS import *

class Game(object):
	def __init__(self):
		self.__init()

	def update(self, screen):
		self.board.draw(screen)
		self.draw_valid_moves(self.valid_moves, screen)
		pygame.display.update()

	def __init(self):
		self.selected = None
		self.board = Board()
		self.turn = RED
		self.valid_moves = {}

	def reset(self):
		self.__init()

	def select(self, row, col):
		if self.selected:
			result = self.__move(row, col)
			if not result:
				self.selected = None
				self.select(row, col)
		
		piece = self.board.get_piece(row, col)
		if piece != 0 and piece.color == self.turn:
			self.selected = piece
			self.valid_moves = self.board.get_valid_moves(piece)
			return True

		return False

	def __move(self, row, col):
		piece = self.board.get_piece(row, col)
		if self.selected and piece == 0 and (row, col) in self.valid_moves:
			self.board.move(self.selected, row, col)
			skipped = self.valid_moves[(row, col)]
			if skipped:
				self.board.remove(skipped)
			self.change_turn()

		else:
			return False

		return True

	def change_turn(self):
		self.valid_moves = {}
		if self.turn == RED:
			self.turn = WHITE
		else:
			self.turn = RED

	def draw_valid_moves(self, moves, screen):
		for move in moves:
			row, col = move
			pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

		