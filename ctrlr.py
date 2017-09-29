#! /usr/bin/python2

class Controller(object):
	"""docstring for Controller"""
	def __init__(self, name, player_ordinality):
		self.name = name
		self.player_ordinality = player_ordinality
		self.stats = {"t":0}

	def output(self, state):
		raise NotImplementedError()
