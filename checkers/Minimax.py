from .CONSTANTS import *
from .board import Board
from copy import deepcopy
import numpy as np
from .board_method import *

# all method that don't have _ in the first letter is old Algorithm
class Minimax:
	def __init__(self, color: tuple[int, int, int] = WHITE) -> None:
		self.color = color
		if self.color == RED:
			self.opposite = WHITE
		else:
			self.opposite = RED

	def evaluate(self, board: np.ndarray):
		# return get_metrics(compress(board)[0])[0]
		return len(board.pieces[self.color]) - len(board.pieces[self.opposite]) + (len(board.kings[self.color]) - len(board.kings[self.opposite]))/2
	
	def _evaluate(self, board):
		# if np.sum(board==1) - np.sum(board==-1) == 1:
		# 	print(board)
		# 	print(depth)

		# return np.sum(board>0) - np.sum(board<0) 

		return get_metrics(compress(board)[0])

	def move(self, board: Board):
		# board_matrix = board.to_matrix()

		value, new_board = self.minimax(board, 3, True)

		# value, new_board = self.minimax(board_matrix, 3, True)


		return new_board

	def _move(self, board: Board):

		board_matrix = board.to_matrix()

		# value, new_board = self.minimax(board, 3, True)

		value, new_board = self._minimax(board_matrix, 4, float('-inf'), float('inf'), True)


		return new_board

	def simulate_move(self, piece, move, board: Board, skip):
		board.move(piece, move[0], move[1])

		if skip:
			board.remove(skip)
		
		return board

	def get_all_boards(self, board: Board, color):
		boards: list[Board] = []

		for piece in board.pieces[color]:
			valid_moves = board.get_valid_moves(piece)

			for move, skip in valid_moves.items():
				temp_board = deepcopy(board)

				temp_piece = temp_board.get_piece(piece.row, piece.col)
				temp_skip = [temp_board.get_piece(p.row, p.col) for p in skip]
				new_board = self.simulate_move(temp_piece, move, temp_board, temp_skip)

				boards.append(deepcopy(new_board))
		
		return boards

	def _minimax(self, board, depth, alpha, beta, maximizing):
		if possible_moves(board) == 0 or game_winner(board) != 0:
			if maximizing:
				return float('-inf'), board
			else:
				return float('inf'), reverse(board)
		
		
		if depth == 0 or game_winner(board) != 0:
			if not maximizing:
				board = reverse(board)

			value, b = self._evaluate(board), board

			return value, b

		
		
		if maximizing:
			maxEval = float('-inf')
			best_board = np.array([])
			for _board in generate_next(board):
				_board = expand(_board)
				eval = self._minimax(reverse(_board), depth-1, alpha, beta, False)[0]
				alpha = max(alpha, eval)
				
				if eval > maxEval:
					maxEval = eval
					best_board = _board.copy()

				if beta <= alpha:
					break
			
			return maxEval, best_board
		
		else:
			minEval = float('inf')
			worst_board = np.array([])
			
			for _board in generate_next(board):
				_board = expand(_board)
				eval = self._minimax(reverse(_board), depth-1, alpha, beta, True)[0]
				beta = min(beta, eval)
				
				if eval < minEval:
					minEval = eval
					worst_board = _board.copy()
				
				if beta <= alpha:
					break
			

			return minEval, worst_board

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



