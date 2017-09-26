#! /usr/bin/python2

class Controller(object):
	"""docstring for Controller"""
	def __init__(self, name):
		self.name = name


	def output(self, state):
		raise NotImplementedError()
