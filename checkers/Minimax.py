from .CONSTANTS import *
from .board import Board

class Minimax:
	def __init__(self, color: tuple[int, int, int] = WHITE) -> None:
		self.color = color
		if self.color == RED:
			self.opposite = WHITE
		else:
			self.opposite = RED

	def evaluate(self, board: Board):
		return len(board.pieces[self.color]) - len(board.pieces[self.opposite]) + (len(board.kings[self.color]) - len(board.kings[self.opposite]))/2
	

	def play(self):
		pass

