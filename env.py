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
		state.grid = ( (self.TILE_EMPTY)*dim[1] for i in dim[0] )


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
			if TILE_EMPTY in col:
				move_positions.append(col.index(TILE_EMPTY),i)

		return move_positions


	@classmethod
	def get_state_on_move(cls, state_cur, move):
		player, pos = move

		grid = [ list(row) for row in state_cur.grid ]

		if player == PLAYER_A:
			grid[pos[0]][pos[1]] = TILE_A
		elif player == PLAYER_B:
			grid[pos[0]][pos[1]] = TILE_B

		state_new = cls.get_state_from_grid(grid)
		return state_new



class Env(object):
	"""docstring for Env"""
	def __init__(self, dim):
		self.dim = dim
		self.state = State(self.dim)
