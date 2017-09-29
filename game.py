#! /usr/bin/python2

from state import State

class Game(object):
	"""docstring for Env"""

	GAME_ON = 0
	GAME_DRAW = 1
	GAME_WIN_A = 2
	GAME_WIN_B = 3


	def __init__(self, dim, min_length, controller_A, controller_B, first):
		self.dim = dim
		self.state = State(self.dim, min_length)

		self.status = self.GAME_ON

		self.controller_A = controller_A
		self.controller_B = controller_B
		
		if first == 0:
			self.state.player_last = controller_B.player_ordinality	# First move by controller_A
		else:
			self.state.player_last = controller_A.player_ordinality	# First move by controller_B

		self.on_move_success = lambda state,move:None
		self.on_move_failure = lambda state,move:None


	def make_move(self, move):
		if not State.is_move_legal(self.state, move):
			self.on_move_failure(self.state, move)
			return

		self.state = State.get_state_on_move(self.state, move)
		self.on_move_success(self.state, move)


	def run(self):
		while self.status == self.GAME_ON:

			if State.is_state_aligned(self.state):
				if self.state.player_last == State.PLAYER_A:
					self.status = self.GAME_WIN_A
				else:
					self.status = self.GAME_WIN_B

			elif State.is_state_full(self.state):
				self.status = self.GAME_DRAW

			else:
				if self.state.player_last == State.PLAYER_A:
					move = self.controller_B.output(self.state)
					self.make_move(move)
				else:
					move = self.controller_A.output(self.state)
					self.make_move(move)

		return self.status
