#! /usr/bin/python2

import time
import random

from ctrlr import Controller
from state import State

class ControllerMinMax(Controller):
	"""docstring for ControllerMinMax"""

	def __init__(self, name, player_ordinality, precalc_utivals_enabled=True, move_randomize=True):
		super(ControllerMinMax, self).__init__(name, player_ordinality)
		self.stats["d"] = 0
		self.stats["n"] = 0

		self.precalc_utivals_enabled = precalc_utivals_enabled
		self.move_randomize = move_randomize

		if self.precalc_utivals_enabled == True:
			self.precalc_utivals_dict = {}
			self.update_precalc_utivals_dict()


	def output(self, state):
		time_init = time.time()

		move_positions = State.get_move_positions(state)

		utivals = None
		if self.precalc_utivals_enabled == True:
			utivals = self.precalc_utivals_dict.get(state, None)

		if utivals == None:
			utivals = []
			for pos in move_positions:
				state_new = State.get_state_on_move(state, (self.player_ordinality, pos))
				utival = self.minmax(state_new, 0)
				utivals.append(utival)

		move_positions_best = None
		if self.player_ordinality == State.PLAYER_A:
			utival_best = float("-inf")
			for i,utival in enumerate(utivals):
				if utival > utival_best:
					utival_best = utival
					move_positions_best = [move_positions[i]]
				elif utival == utival_best:
					move_positions_best.append(move_positions[i])
		else:
			utival_best = float("inf")
			for i,utival in enumerate(utivals):
				if utival < utival_best:
					utival_best = utival
					move_positions_best = [move_positions[i]]
				elif utival == utival_best:
					move_positions_best.append(move_positions[i])

		if self.move_randomize == True:
			pos = random.choice(move_positions_best)
		else:
			pos = move_positions_best[0]

		time_end = time.time()
		self.stats["t"] += time_end - time_init

		return (self.player_ordinality, pos)


	def minmax(self, state, stack_depth):
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
				utival = self.minmax(state_new, stack_depth+1)

				if player_cur == State.PLAYER_A:
					if utival > utival_best:
						utival_best = utival
				else:
					if utival < utival_best:
						utival_best = utival

			return utival_best


	def update_precalc_utivals_dict(self):

		s = State((4,4),3)
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1,1,1,1)


		grid = ((1, 0, 0, 0), (2, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1,1,1,-1)

		grid = ((1, 2, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1, 1, -1, -1)

		grid = ((1, 0, 2, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, -1, 1, -1)

		grid = ((1, 0, 0, 2), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1, 1, 1, -1)


		grid = ((2, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1, 1, 1, 1)

		grid = ((0, 1, 0, 0), (0, 2, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, 1, 1, -1)

		grid = ((0, 1, 2, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, 1, 1, -1)

		grid = ((0, 1, 0, 2), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1, 1, 1, 1)


		grid = ((2, 0, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1, 1, 1, 1)

		grid = ((0, 2, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, 1, 1, -1)

		grid = ((0, 0, 1, 0), (0, 0, 2, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, 1, 1, -1)

		grid = ((0, 0, 1, 2), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (1, 1, 1, 1)


		grid = ((2, 0, 0, 1), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, 1, 1, 1)

		grid = ((0, 2, 0, 1), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, 1, -1, -1)

		grid = ((0, 0, 2, 1), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, -1, 1, 1)

		grid = ((0, 0, 0, 1), (0, 0, 0, 2), (0, 0, 0, 0), (0, 0, 0, 0))
		s = State.get_state_from_grid(grid)
		s.min_length = 3
		s.player_last = State.PLAYER_B
		self.precalc_utivals_dict[s] = (-1, 1, 1, 1)
