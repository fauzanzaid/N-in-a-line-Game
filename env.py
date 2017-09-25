#! /usr/bin/python2



class State(object):
	"""docstring for State"""

	TILE_EMPTY = 0
	TILE_A = 1
	TILE_B = 2


	def __init__(self, dim):
		self.dim = dim
		self.grid = None

		self.create_grid(self.dim)


	def create_grid(self, dim):
		self.grid = [ [self.TILE_EMPTY]*dim[1] for i in dim[0] ]
		


class Env(object):
	"""docstring for Env"""
	def __init__(self, dim):
		self.dim = dim
		self.state = State(self.dim)
