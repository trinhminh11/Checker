import numpy as np

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def num_captured(board):
	return 12 - np.sum(board < 0)

def num_branches(board, x, y):
	count = 0
	if (board[x, y] >= 1 and x < 6):
		if (y < 6):
			if (board[x+1, y+1] < 0 and board[x+2, y+2] == 0):
				board[x+2, y+2] = board[x, y]
				board[x, y] = 0
				temp = board[x+1, y+1]
				board[x+1, y+1] = 0
				count += num_branches(board, x+2, y+2) + 1
				board[x+1, y+1] = temp
				board[x, y] = board[x+2, y+2]
				board[x+2, y+2] = 0
		if (y > 1):
			if (board[x+1, y-1] < 0 and board[x+2, y-2] == 0):
				board[x+2, y-2] = board[x, y]
				board[x, y] = 0
				temp = board[x+1, y-1]
				board[x+1, y-1] = 0
				count += num_branches(board, x+2, y-2) + 1
				board[x+1, y-1] = temp
				board[x, y] = board[x+2, y-2]
				board[x+2, y-2] = 0
	if (board[x, y] == 3 and x > 0):
		if (y < 6):
			if (board[x-1, y+1] < 0 and board[x-2, y+2] == 0):
				board[x-2, y+2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y+1]
				board[x-1, y+1] = 0
				count += num_branches(board, x-2, y+2) + 1
				board[x-1, y+1] = temp
				board[x, y] = board[x-2, y+2]
				board[x-2, y+2] = 0
		if (y > 1):
			if (board[x-1, y-1] < 0 and board[x-2, y-2] == 0):
				board[x-2, y-2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y-1]
				board[x-1, y-1] = 0
				count += num_branches(board, x-2, y-2) + 1
				board[x-1, y-1] = temp
				board[x, y] = board[x-2, y-2]
				board[x-2, y-2] = 0
	return count

def possible_moves(board):
	count = 0
	for i in range(0, 8):
		for j in range(0, 8):
			if (board[i, j] > 0):
				count += num_branches(board, i, j)
	if (count > 0):
		return count
	for i in range(0, 8):
		for j in range(0, 8):
			if (board[i, j] >= 1 and i < 7):
				if (j < 7):
					count += (board[i+1, j+1] == 0)
				if (j > 0):
					count += (board[i+1, j-1] == 0)
			if (board[i, j] == 3 and i > 0):
				if (j < 7):
					count += (board[i-1, j+1] == 0)
				elif (j > 0):
					count += (board[i-1, j-1] == 0)
	return count


def game_winner(board):
	if (np.sum(board < 0) == 0):
		return 1
	elif (np.sum(board > 0) == 0):
		return -1
	if (possible_moves(board) == 0):
		return -1
	elif (possible_moves(reverse(board)) == 0):
		return 1
	else:
		return 0

def at_enemy(board):
	count = 0
	for i in range(5, 8):
		count += np.sum(board[i] == 1) + np.sum(board[i] == 3)
	return count

def at_middle(board):
	count = 0
	for i in range(3, 5):
		count += np.sum(board[i] == 1) + np.sum(board[i] == 3)
	return count

def num_pawn(board):
	return np.sum(board == 1)

def num_kings(board):
	return np.sum(board == 3)

def capturables(board): # possible number of unsupported enemies
	count = 0
	for i in range(1, 7):
		for j in range(1, 7):
			if (board[i, j] < 0):
				count += (board[i+1, j+1] >= 0 and board[i+1, j-1] >= 0 and  board[i-1, j+1] >= 0 and board[i-1, j-1] >= 0)
	return count

def semicapturables(board): # number of own units with at least one support
	return (12 - uncapturables(board) - capturables(reverse(board)))

def uncapturables(board): # number of own units that can't be captured
	count = 0
	for i in range(1, 7):
		for j in range(1, 7):
			if (board[i, j] > 0):
				count += ((board[i+1, j+1] > 0 < board[i+1, j-1]) or (board[i-1, j+1] > 0 < board[i-1, j-1]) or (board[i+1, j+1] > 0 < board[i-1, j+1]) or (board[i+1, j-1] > 0 < board[i-1, j-1]))
	count += np.sum(board[0] == 1) + np.sum(board[0] == 3) + np.sum(board[1:7, 0] == 1) + np.sum(board[1:7, 0] == 3) + np.sum(board[7] == 1) + np.sum(board[7] == 3) + np.sum(board[1:7, 7] == 1) + np.sum(board[1:7, 7] == 3)
	return count

def reverse(board):
	b = -board
	b = np.fliplr(b)
	b = np.flipud(b)
	return b

def get_metrics(board): # returns [label, 10 labeling metrics]
	'''
	return [score, captured, potential, num_pawn, num_king, num_captureable, semi_capturable, num_uncaptureable, num_piece at middle, num_piece at enemy, game_state]
	'''
	b = expand(board)

	capped = num_captured(b) - num_captured(reverse(b))
	potential = possible_moves(b) - possible_moves(reverse(b))
	pawn = num_pawn(b) - num_pawn(reverse(b))
	kings = num_kings(b) - num_kings(reverse(b))
	caps = capturables(b) - capturables(reverse(b))
	semicaps = semicapturables(b) - semicapturables(reverse(b))
	uncaps = uncapturables(b) - uncapturables(reverse(b))
	mid = at_middle(b) - at_middle(reverse(b))
	far = at_enemy(b) - at_enemy(reverse(b))
	won = game_winner(b)

	score = (5*capped + potential + 5*pawn + 10*kings + 5*caps + 4*uncaps + 1/2*mid + 2*far + 1000*won)


	# score = sigmoid(score)

	return score

	# return np.array([score, capped, potential, pawn, kings, caps, semicaps, uncaps, mid, far, won])



def np_board():
	return np.array(get_board())

def get_board():
	return [1, 1, 1, 1,  1, 1, 1, 1,  1, 1, 1, 1,  0, 0, 0, 0,  0, 0, 0, 0,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1]

def expand(board):
	b = np.zeros((8, 8), dtype='b')
	for i in range(0, 8):
		if (i%2 == 0):
			b[i] = np.array([0, board[i*4], 0, board[i*4 + 1], 0, board[i*4 + 2], 0, board[i*4 + 3]])
		else:
			b[i] = np.array([board[i*4], 0, board[i*4 + 1], 0, board[i*4 + 2], 0, board[i*4 + 3], 0])
	return b

def compress(board):
	b = np.zeros((1,32))
	for i in range(0, 8):
		if (i%2 == 0):
			b[0, i*4 : i*4+4] = np.array([board[i, 1], board[i, 3], board[i, 5], board[i, 7]])
		else:
			b[0, i*4 : i*4+4] = np.array([board[i, 0], board[i, 2], board[i, 4], board[i, 6]])
	return b

def generate_branches(board, x, y):
	bb = compress(board)

	if (board[x, y] >= 1 and x < 6):
		temp_1 = board[x, y]
		if (y < 6):
			if (board[x+1, y+1] < 0 and board[x+2, y+2] == 0):
				board[x+2, y+2] = board[x, y]
				if (x+2 == 7):
					board[x+2, y+2] = 3
				temp = board[x+1, y+1]
				board[x+1, y+1] = 0
				if (board[x, y] != board[x+2, y+2]):
					board[x, y] = 0
					bb = np.vstack((bb, compress(board)))
				else:
					board[x, y] = 0
					bb = np.vstack((bb, generate_branches(board, x+2, y+2)))
				board[x+1, y+1] = temp
				board[x, y] = temp_1
				board[x+2, y+2] = 0

		if (y > 1):
			if (board[x+1, y-1] < 0 and board[x+2, y-2] == 0):
				board[x+2, y-2] = board[x, y]
				if (x+2 == 7):
					board[x+2, y-2] = 3
				temp = board[x+1, y-1]
				board[x+1, y-1] = 0
				if (board[x, y] != board[x+2, y-2]):
					board[x, y] = 0
					bb = np.vstack((bb, compress(board)))
				else:
					board[x, y] = 0
				bb = np.vstack((bb, generate_branches(board, x+2, y-2)))
				board[x+1, y-1] = temp
				board[x, y] = temp_1
				board[x+2, y-2] = 0

	if (board[x, y] == 3 and x > 0):
		if (y < 6):
			if (board[x-1, y+1] < 0 and board[x-2, y+2] == 0):
				board[x-2, y+2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y+1]
				board[x-1, y+1] = 0
				bb = np.vstack((bb, generate_branches(board, x-2, y+2)))
				board[x-1, y+1] = temp
				board[x, y] = board[x-2, y+2]
				board[x-2, y+2] = 0
		if (y > 1):
			if (board[x-1, y-1] < 0 and board[x-2, y-2] == 0):
				board[x-2, y-2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y-1]
				board[x-1, y-1] = 0
				bb = np.vstack((bb, generate_branches(board, x-2, y-2)))
				board[x-1, y-1] = temp
				board[x, y] = board[x-2, y-2]
				board[x-2, y-2] = 0
	return bb

def generate_next(board):

	bb = np.array([get_board()])
	for i in range(0, 8):
		for j in range(0, 8):
			if (board[i, j] > 0):
				bb = np.vstack((bb, generate_branches(board, i, j)[1:]))
	
	
	for i in range(0, 8):
		for j in range(0, 8):
			if (board[i, j] >= 1 and i < 7):
				temp = board[i, j]

				if (j > 0):
					if (board[i+1, j-1] == 0):
						board[i+1, j-1] = board[i, j]
						if (i+1 == 7):
							board[i+1, j-1] = 3
						board[i, j] = 0
						bb = np.vstack((bb, compress(board)))
						board[i, j] = temp
						board[i+1, j-1] = 0

				if (j < 7):
					if (board[i+1, j+1] == 0):
						board[i+1, j+1] = board[i, j]
						if (i+1 == 7):
							board[i+1, j+1] = 3
						board[i, j] = 0
						bb = np.vstack((bb, compress(board)))
						board[i, j] = temp
						board[i+1, j+1] = 0
				
			if (board[i, j] == 3 and i > 0):
				if (j > 0):
					if (board[i-1, j-1] == 0):
						board[i-1, j-1] = board[i, j]
						board[i, j] = 0
						bb = np.vstack((bb, compress(board)))
						board[i, j] = board[i-1, j-1]
						board[i-1, j-1] = 0
				elif (j < 7):
					if (board[i-1, j+1] == 0):
						board[i-1, j+1] = board[i, j]
						board[i, j] = 0
						bb = np.vstack((bb, compress(board)))
						board[i, j] = board[i-1, j+1]
						board[i-1, j+1] = 0
	
	
	return bb[1:]

def random_board():
	b = get_board()
	promote = 0.9
	remove = 0.4
	add = 0
	for piece in b:
		# randomly promote, remove, or add piece
		rand = np.random.random()
		if piece is not 0 and rand > promote:
			piece = piece * 3
			promote = promote + 0.005
		elif piece is not 0 and rand < remove:
			piece = 0
			remove = remove - 0.025
			add = add + 0.05
		elif piece is 0 and rand < add:
			if np.random.random() > 0.5:
				piece = 1
			else:
				piece = -1
	return b





# board = np.array([[ 0,  1,  0,  1,  0,  1,  0,  1],
# 				[ 1,  0,  1,  0,  1,  0,  1,  0],
# 				[ 0,  1,  0,  1,  0,  1,  0,  1],
# 				[ 0,  0,  0,  0, -1,  0,  0,  0],
# 				[ 0,  0,  0,  0,  0,  0,  0,  0],
# 				[-1,  0, -1,  0,  0,  0, -1,  0],
# 				[ 0, -1,  0, -1,  0, -1,  0,  0],
# 				[-1,  0, -1,  0, -1,  0, -1,  0]])

# boards = generate_branches(board, 2, 1)


# board = compress(board)

# print(board)

# boards = generate_next(board)

# for b in boards:
# 	print(expand(b))

# 	print("------------------")

# board = np.array(  [[ 0,  1,  0,  1,  0,  1,  0,  1],
# 					[ 1,  0,  1,  0,  1,  0,  1,  0],
# 					[ 0,  0,  0,  1,  0,  1,  0,  1],
# 					[ 1,  0,  0,  0,  0,  0,  0,  0],
# 					[ 0, -1,  0,  0,  0,  0,  0,  0],
# 					[ 0,  0, -1,  0, -1,  0, -1,  0],
# 					[ 0, -1,  0, -1,  0, -1,  0, -1],
# 					[-1,  0, -1,  0, -1,  0, -1,  0]])



# boards = generate_next(board)

# for board in boards:
# 	print(expand(board))
# 	print("---------------")