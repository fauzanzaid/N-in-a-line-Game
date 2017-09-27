#! /usr/bin/python2

from ctrlr import Controller

class ControllerManual(Controller):
	"""docstring for ControllerManual"""
	def __init__(self, name, get_pos):
		super(ControllerManual, self).__init__(name)
		self.get_pos = get_pos


	def output(self, state):
		pos = self.get_pos(state)
		return (self.player_ordinality, pos)