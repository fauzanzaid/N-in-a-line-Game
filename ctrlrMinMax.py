#! /usr/bin/python2

from ctrlr import Controller

class ControllerMinMax(Controller):
	"""docstring for ControllerMinMax"""
	def __init__(self, arg):
		super(ControllerMinMax, self).__init__()
		self.arg = arg
