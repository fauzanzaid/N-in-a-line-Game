#! /usr/bin/python2

from ctrlr import Controller
from state import State

class ControllerMinMax(Controller):
	"""docstring for ControllerMinMax"""

	UTIVAL_DRAW = 0
	UTIVAL_WIN_A = 1
	UTIVAL_WIN_B = -1

	def __init__(self, , name, player_ordinality):
		super(ControllerMinMax, self).__init__(name, player_ordinality)


	def output(self, state):
		move_positions = State.get_move_postions(state)
		utivals = []

		for pos in move_positions:
			state_new = get_state_on_move(state, (self.player_ordinality, pos))
			utival = minmax()
			utivals.append(utival)

		pos = None
		if player_ordinality == State.PLAYER_A:
			pos = move_positions[ utivals.index(max(utivals)) ]
		else:
			pos = move_positions[ utivals.index(max(utivals)) ]

		return (player_ordinality, pos)


	def minmax(self, state):
		pass