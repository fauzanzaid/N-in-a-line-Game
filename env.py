#! /usr/bin/python2



class State(object):
	"""docstring for State"""

	TILE_EMPTY = 0
	TILE_A = 1
	TILE_B = 2


	def __init__(self, dim):
		self.dim = dim
		self.grid = None

		self.create_grid(self, self.dim)


	@classmethod
	def create_grid(cls, state, dim):
		state.grid = ( (self.TILE_EMPTY)*dim[1] for i in dim[0] )


	@classmethod
	def get_moves(cls, state):
		moves = []
		grid_transpose = zip(*state.grid)
		
		for i,col in enumerate(grid_transpose):
			if TILE_EMPTY in col:
				moves.append( (i, col.index(TILE_EMPTY)) )

		return moves



class Env(object):
	"""docstring for Env"""
	def __init__(self, dim):
		self.dim = dim
		self.state = State(self.dim)
