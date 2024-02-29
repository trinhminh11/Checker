import pygame
from .board import Board
from .CONSTANTS import *
from .Minimax import Minimax
from reinforced_model import reinforced_model

class Game(object):
	def __init__(self, turn):
		self.__init(turn)

	def update(self, screen):
		self.board.draw(screen)
		self.draw_valid_moves(self.valid_moves, screen)
		
		if self.turn == self.bot.color:
			self.board = self.bot.move(self.board)
			self.change_turn()

		pygame.display.update()

	def __init(self, turn):
		self.selected = None
		self.board = Board()
		self.turn = turn
		self.valid_moves = {}

		self.bot = Minimax()

		# self.bot = reinforced_model.model


	def reset(self, turn):
		self.__init(turn)

	def select(self, row: int, col: int):
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

		else:
			self.valid_moves = {}

		return False

	def __move(self, row: int, col: int):
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

	def draw_valid_moves(self, moves: dict, screen: pygame.Surface):
		for move in moves:
			row, col = move
			pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
		