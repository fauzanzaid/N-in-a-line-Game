#! /usr/bin/python2

from ctrlr import Controller

class ControllerMinMax(Controller):
	"""docstring for ControllerMinMax"""

	UTIVAL_DRAW = 0
	UTIVAL_WIN_A = 1
	UTIVAL_WIN_B = -1

	def __init__(self, , name, player_ordinality):
		super(ControllerMinMax, self).__init__(name, player_ordinality)


	def output(self, state):
		pass


	def minmax(self, state):
		pass