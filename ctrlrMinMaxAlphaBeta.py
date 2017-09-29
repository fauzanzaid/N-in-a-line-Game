#! /usr/bin/python2

import time

from ctrlr import Controller
from state import State

class ControllerMinMaxAlphaBeta(Controller):
	"""docstring for ControllerMinMaxAlphaBeta"""

	def __init__(self, name, player_ordinality):
		super(ControllerMinMaxAlphaBeta, self).__init__(name, player_ordinality)
		self.stats["d"] = 0
		self.stats["n"] = 0


	def output(self, state):
		time_init = time.time()

		move_positions = State.get_move_positions(state)
		utivals = []

		for pos in move_positions:
			state_new = State.get_state_on_move(state, (self.player_ordinality, pos))
			utival = self.minmax(state_new, float("-inf"), float("inf"), 0)
			utivals.append(utival)

		pos = None
		if self.player_ordinality == State.PLAYER_A:
			pos = move_positions[ utivals.index(max(utivals)) ]
		else:
			pos = move_positions[ utivals.index(min(utivals)) ]

		time_end = time.time()
		self.stats["t"] += time_end - time_init

		return (self.player_ordinality, pos)


	def minmax(self, state, alpha, beta, stack_depth):
		self.stats["n"] += 1
		if stack_depth > self.stats["d"]:
			self.stats["d"] = stack_depth

		if State.is_state_terminal(state):
			return State.utility_value(state)

		else:
			utival_best = None
			player_cur = None

			if state.player_last == State.PLAYER_A:
				utival_best = float("inf")
				player_cur = State.PLAYER_B
			else:
				utival_best = float("-inf")
				player_cur = State.PLAYER_A

			move_positions = State.get_move_positions(state)
			for pos in move_positions:
				state_new = State.get_state_on_move(state, (player_cur,pos))
				utival = self.minmax(state_new, alpha, beta, stack_depth+1)

				# max node
				if player_cur == State.PLAYER_A:
					if utival > utival_best:
						utival_best = utival
					if utival > beta:
						return utival
					if utival > alpha:
						alpha = utival

				# min node
				else:
					if utival < utival_best:
						utival_best = utival
					if utival < alpha:
						return utival
					if utival < beta:
						beta = utival

			return utival_best
