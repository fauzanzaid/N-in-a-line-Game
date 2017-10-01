#! /usr/bin/python2

import time

from ctrlrMinMax import ControllerMinMax
from state import State

class ControllerMinMaxAlphaBeta(ControllerMinMax):
	"""docstring for ControllerMinMaxAlphaBeta"""

	def __init__(self, name, player_ordinality, precalc_utivals_enabled = True):
		super(ControllerMinMaxAlphaBeta, self).__init__(name, player_ordinality, precalc_utivals_enabled)


	def minmax(self, state, stack_depth, alpha=float("-inf"), beta=float("inf")):
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
				utival = self.minmax(state_new, stack_depth+1, alpha, beta)

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
