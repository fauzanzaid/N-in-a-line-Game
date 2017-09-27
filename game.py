#! /usr/bin/python2

class Game(object):
	"""docstring for Env"""

	GAME_ON = 0
	GAME_DRAW = 1
	GAME_WIN_A = 2
	GAME_WIN_B = 3


	def __init__(self, dim, min_length, controller_A, controller_B):
		self.dim = dim
		self.state = State(self.dim)
		self.state.min_length = min_length

		self.status = self.GAME_ON
		
		self.controller_A = controller_A
		self.controller_B = controller_B
		self.state.player_last = controller_B.player_ordinality	# First move by controller_A



	def run(self):
		while self.status == self.GAME_ON:
			pass

		return self.status
