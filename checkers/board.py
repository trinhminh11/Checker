import pygame
from .CONSTANTS import *
from .pieces import Piece

class Board(object):
	def __init__(self):
		self.board: list[list[Piece | int]] = []
		self.pieces: dict[tuple[int, int, int], list[Piece]] = {RED: [], WHITE: []}
		self.kings: dict[tuple[int, int, int], list[Piece]] = {RED: [], WHITE: []}

		self.create_board()

	def create_board(self):
		for row in range(ROWS):
			self.board.append([])
			for col in range(COLS):
				if col % 2 == ((row + 1) % 2):
					if row < 3:
						piece = Piece(row, col, WHITE)
						self.board[row].append(piece)
						self.pieces[WHITE].append(piece)
					elif row > 4:
						piece = Piece(row, col, RED)
						self.board[row].append(piece)
						self.pieces[RED].append(piece)
					else:
						self.board[row].append(0)
				else:
					self.board[row].append(0)
	
	def get_pieces(self, color: tuple[int, int, int]):
		return self.pieces[color]
	
	def move(self, piece: Piece, row, col):
		self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
		piece.move(row, col)

		if row == ROWS - 1 or row == 0:
			piece.make_king()
			self.kings[piece.color].append(piece)

	def get_piece(self, row: int, col: int) -> Piece:
		return self.board[row][col]

	def get_valid_moves(self, piece: Piece):
		moves = {}
		left = piece.col - 1
		right = piece.col + 1
		row = piece.row

		
		if piece.color == RED or piece.king:
			moves.update(self.__traverse(row - 1, max(row - 3, -1), -1, piece.color, left, True, king = piece.king))
			moves.update(self.__traverse(row - 1, max(row - 3, -1), -1, piece.color, right, False, king = piece.king))

		if piece.color == WHITE or piece.king:
			moves.update(self.__traverse(row + 1, min(row + 3, ROWS), 1, piece.color, left, True, king = piece.king))
			moves.update(self.__traverse(row + 1, min(row + 3, ROWS), 1, piece.color, right, False, king = piece.king))

		return moves

	def __traverse(self, start, stop, step, color, col, isleft: bool, skipped = None, king = False):
		if skipped == None:
			skipped = []
		
		moves = {}
		last = []

		for r in range(start, stop, step):
			if col < -1 or col >= COLS:
				break

			current = self.board[r][col]

			if current == 0:
				if skipped:
					if last:
						moves[(r, col)] = last + skipped
					else:
						break
				else:
					moves[(r, col)] = last
				
				if last:
					row = max(r-3, -1)
					reverse = min(r+3, ROWS)
				
					if step == 1:
						row, reverse = reverse, row
					
					moves.update(self.__traverse(r+step, row, step, color, col-1, True, skipped=skipped + last, king = king))
					moves.update(self.__traverse(r+step, row, step, color, col+1, False, skipped=skipped + last, king = king))

					if king:
						if isleft:
							moves.update(self.__traverse(r-step, reverse, -step, color, col-1, True, skipped=skipped + last, king = king))
						else:
							moves.update(self.__traverse(r-step, reverse, -step, color, col+1, False, skipped=skipped + last, king = king))
						
				break

			elif current.color == color:
				break
			else:
				last = [current]
			
			if isleft:
				col -= 1
			else:
				col += 1
		
		return moves

	def remove(self, pieces: list[Piece]):
		for piece in pieces:
			self.board[piece.row][piece.col] = 0
			if piece != 0:
				color = piece.color
				self.pieces[color].remove(piece)
				if piece.king:
					self.kings[color].remove(piece)

	def winner(self):
		if len(self.pieces[RED]) <= 0:
			return WHITE
		elif len(self.pieces[WHITE]) <= 0:
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