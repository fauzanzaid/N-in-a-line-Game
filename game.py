#! /usr/bin/python2

from state import State

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
			if State.is_state_full(self.state):
				self.status = self.GAME_DRAW

			elif State.is_state_aligned(self.state):
				if self.state.player_last == State.PLATER_A:
					self.status = self.GAME_WIN_A
				else:
					self.status = self.GAME_WIN_B

			else:
				if self.status,player_last == State.PLATER_A:
					pass
				else:
					pass

		return self.status
