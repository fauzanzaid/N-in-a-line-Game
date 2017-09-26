#! /usr/bin/python2



class State(object):
	"""docstring for State"""

	PLAYER_A = 0
	PLAYER_B = 1

	TILE_EMPTY = 0
	TILE_A = 1
	TILE_B = 2


	def __init__(self, dim):
		self.dim = dim
		self.grid = None

		if dim:
			self.create_grid(self, self.dim)


	@classmethod
	def create_grid(cls, state, dim):
		state.grid = tuple( (cls.TILE_EMPTY,)*dim[1] for i in xrange(dim[0]) )


	@classmethod
	def get_state_from_grid(cls, grid):
		state = cls(None)
		state.dim = len(grid), len(grid[0])
		state.grid = tuple( tuple(row) for row in grid )
		return state


	@classmethod
	def get_move_positions(cls, state):
		move_positions = []
		grid_transpose = zip(*state.grid)
		
		for i,col in enumerate(grid_transpose):
			if cls.TILE_EMPTY in col:
				move_positions.append((col.index(cls.TILE_EMPTY),i))

		return move_positions


	@classmethod
	def get_state_on_move(cls, state_cur, move):
		player, pos = move
		grid = [ list(row) for row in state_cur.grid ]

		if player == cls.PLAYER_A:
			grid[pos[0]][pos[1]] = cls.TILE_A
		elif player == cls.PLAYER_B:
			grid[pos[0]][pos[1]] = cls.TILE_B

		state_new = cls.get_state_from_grid(grid)
		return state_new


	@classmethod
	def is_state_full(cls, state):
		for row in state.grid:
			for tile in row:
				if tile == cls.TILE_EMPTY:
					return False
		return True


	@classmethod
	def num_inline_hor(cls, state, pos):
		tile_ref = state.grid[pos[0]][pos[1]]
		length = 1

		# Check to the left
		pos_chk = [pos[0], pos[1]-1]
		while True:
			if pos_chk[1] < 0:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[1] -= 1

		# Check to the right
		pos_chk = [pos[0], pos[1]+1]
		while True:
			if pos_chk[1] > state.dim[1]-1:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[1] += 1

		return length


	@classmethod
	def num_inline_ver(cls, state, pos):
		tile_ref = state.grid[pos[0]][pos[1]]
		length = 1

		# Check upwards
		pos_chk = [pos[0]-1, pos[1]]
		while True:
			if pos_chk[0] < 0:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[0] -= 1

		# Check downwards
		pos_chk = [pos[0]+1, pos[1]]
		while True:
			if pos_chk[0] > state.dim[0]-1:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[0] += 1

		return length


	@classmethod
	def num_inline_dia_up(cls, state, pos):
		tile_ref = state.grid[pos[0]][pos[1]]
		length = 1

		# Check up, right
		pos_chk = [pos[0]-1, pos[1]+1]
		while True:
			if pos_chk[0] < 0 or pos_chk[1] > state.dim[1]-1:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[0] -= 1
				pos_chk[1] += 1

		# Check down, left
		pos_chk = [pos[0]+1, pos[1]-1]
		while True:
			if pos_chk[0] > state.dim[0]-1 or pos_chk[1] < 0:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[0] += 1
				pos_chk[1] -= 1

		return length


	@classmethod
	def num_inline_dia_down(cls, state, pos):
		tile_ref = state.grid[pos[0]][pos[1]]
		length = 1

		# Check up, right
		pos_chk = [pos[0]+1, pos[1]+1]
		while True:
			if pos_chk[0] > state.dim[0]-1 or pos_chk[1] > state.dim[1]-1:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[0] += 1
				pos_chk[1] += 1

		# Check down, left
		pos_chk = [pos[0]-1, pos[1]-1]
		while True:
			if pos_chk[0] < 0 or pos_chk[1] < 0:
				break
			elif state.grid[pos_chk[0]][pos_chk[1]] != tile_ref:
				break
			else:
				length += 1
				pos_chk[0] -= 1
				pos_chk[1] -= 1

		return length


	@classmethod
	def pretty_print(cls, state):
		for row in state.grid:
			for tile in row:
				if tile == cls.TILE_EMPTY:
					print "-",
				elif tile == cls.TILE_A:
					print "A",
				elif tile == cls.TILE_B:
					print "B",
			print ""



class Env(object):
	"""docstring for Env"""
	def __init__(self, dim):
		self.dim = dim
		self.state = State(self.dim)
