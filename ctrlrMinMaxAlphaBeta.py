#! /usr/bin/python2

from ctrlr import Controller

class ControllerMinMaxAlphaBeta(Controller):
	"""docstring for ControllerMinMaxAlphaBeta"""
	def __init__(self, arg):
		super(ControllerMinMaxAlphaBeta, self).__init__()
		self.arg = arg
