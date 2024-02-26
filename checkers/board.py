import pygame
from .CONSTANTS import *
from .pieces import Piece

class Board(object):
	def __init__(self):
		self.board: list[list[Piece | int]] = []
		self.red_left = 12
		self.white_left = 12
		self.red_king = 0
		self.white_king = 0
		self.create_board()



	def create_board(self):
		for row in range(ROWS):
			self.board.append([])
			for col in range(COLS):
				if col % 2 == ((row + 1) % 2):
					if row < 3:
						self.board[row].append(Piece(row, col, WHITE))
					elif row > 4:
						self.board[row].append(Piece(row, col, RED))
					else:
						self.board[row].append(0)
				else:
					self.board[row].append(0)

	def move(self, piece: Piece, row, col):
		self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
		piece.move(row, col)

		if row == ROWS - 1 or row == 0:
			piece.make_king()
			if piece.color == WHITE:
				self.white_king += 1
			else:
				self.red_king += 1

	def get_piece(self, row: int, col: int) -> Piece:
		return self.board[row][col]

	def get_valid_moves(self, piece: Piece):
		moves = {}
		left = piece.col - 1
		right = piece.col + 1
		row = piece.row

		if piece.king:
			moves.update(self.__traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
			moves.update(self.__traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
			moves.update(self.__traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
			moves.update(self.__traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

		else:
			if piece.color == RED:
				moves.update(self.__traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
				moves.update(self.__traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

			if piece.color == WHITE:
				moves.update(self.__traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
				moves.update(self.__traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

		return moves
			

	def __traverse_left(self, start, stop, step, color, left: int, skipped = None):
		if skipped == None:
			skipped = []

		moves = {}
		last = []
		for r in range(start, stop, step):
			if left < -1:
				break

			current = self.board[r][left]
			if current == 0:
				if skipped:
					if  last:
						moves[(r, left)] = last + skipped
					else:
						break
				else:
					moves[(r, left)] = last

				if last:
					if step == -1:
						row = max(r - 3, -1)
					else:
						row = min(r + 3, ROWS)

					moves.update(self.__traverse_left(r + step, row, step, color, left - 1, skipped = skipped + last))
					moves.update(self.__traverse_right(r + step, row, step, color,left + 1, skipped = skipped + last))
				break
			elif current.color == color:
				break
			else:
				last = [current]
			left -= 1

		return moves

	def __traverse_right(self, start, stop, step, color, right: int, skipped = None):
		if skipped == None:
			skipped = []

		moves = {}
		last = []
		for r in range(start, stop, step):
			if right >= COLS:
				break

			current = self.board[r][right]
			if current == 0:
				if skipped:
					if last:
						moves[(r, right)] = last + skipped
					
					else:
						break
				else:
					moves[(r, right)] = last

				if last:
					if step == -1:
						row = max(r - 3, -1)
					else:
						row = min(r + 3, ROWS)

					moves.update(self.__traverse_left(r + step, row, step, color, right - 1, skipped = skipped + last))
					moves.update(self.__traverse_right(r + step, row, step, color, right + 1, skipped = skipped + last))
				break

			elif current.color == color:
				break

			else:
				last = [current]

			right += 1

		return moves
	
	def remove(self, pieces: list[Piece]):
		for piece in pieces:
			self.board[piece.row][piece.col] = 0
			if piece != 0:
				if piece.color == RED:
					self.red_left -= 1
				else:
					self.white_left -= 1

	def winner(self):
		if self.red_left <= 0:
			return WHITE
		elif self.white_left <= 0:
			return RED

		return None

	def draw_board(self, screen: pygame.Surface):
		screen.fill(BLACK)

		for row in range(ROWS):
			for col in range((row) % 2, COLS, 2):
				pygame.draw.rect(screen, WHITE, (row*SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

	def draw(self, screen: pygame.Surface):
		self.draw_board(screen)
		for row in range(ROWS):
			for col in range(COLS):
				piece = self.board[row][col]
				if piece != 0:
					piece.draw(screen)