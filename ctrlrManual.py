#! /usr/bin/python2

from ctrlr import Controller

class ControllerManual(Controller):
	"""docstring for ControllerManual"""
	def __init__(self, arg):
		super(ControllerManual, self).__init__()
		self.arg = arg
		