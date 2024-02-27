from .CONSTANTS import *
from .board import Board
from copy import deepcopy

class Minimax:
	def __init__(self, color: tuple[int, int, int] = WHITE) -> None:
		self.color = color
		if self.color == RED:
			self.opposite = WHITE
		else:
			self.opposite = RED

	def evaluate(self, board: Board):
		return len(board.pieces[self.color]) - len(board.pieces[self.opposite]) + (len(board.kings[self.color]) - len(board.kings[self.opposite]))/2
	

	def move(self, board):
		value, new_board = self.minimax(board, 3, True)

		return new_board

		return

	def simulate_move(self, piece, move, board: Board, skip):

		board.move(piece, move[0], move[1])

		if skip:
			board.remove(skip)
		
		return board

	def get_all_boards(self, board: Board, color):
		boards = []


		for piece in board.pieces[color]:
			valid_moves = board.get_valid_moves(piece)

			for move, skip in valid_moves.items():
				temp_board = deepcopy(board)

				temp_piece = temp_board.get_piece(piece.row, piece.col)
				temp_skip = [temp_board.get_piece(p.row, p.col) for p in skip]
				new_board = self.simulate_move(temp_piece, move, temp_board, temp_skip)

				boards.append(deepcopy(new_board))

		
		return boards

	def minimax(self, board: Board, depth, maximizing):
		if depth == 0 or board.winner():
			return self.evaluate(board), board
		
		if maximizing:
			maxEval = float('-inf')
			best_board = None
			for _board in self.get_all_boards(board, self.color):
				eval = self.minimax(_board, depth-1, False)[0]
				if eval > maxEval:
					maxEval = eval
					best_board = _board
			
			return maxEval, best_board
		
		else:
			minEval = float('inf')
			worst_board = None
			for _board in self.get_all_boards(board, self.opposite):
				eval = self.minimax(_board, depth-1, True)[0]
				if eval < minEval:
					minEval = eval
					worst_board = _board
			
			return minEval, worst_board

