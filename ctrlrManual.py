#! /usr/bin/python2

import time

from ctrlr import Controller

class ControllerManual(Controller):
	"""docstring for ControllerManual"""
	def __init__(self, name, player_ordinality, get_pos):
		super(ControllerManual, self).__init__(name, player_ordinality)
		self.get_pos = get_pos


	def output(self, state):
		time_init = time.time()

		pos = self.get_pos(state)

		time_end = time.time()
		self.stats["t"] += time_end - time_init

		return (self.player_ordinality, pos)
