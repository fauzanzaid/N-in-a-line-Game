#! /usr/bin/python2

import turtle

class GUI(object):
	"""docstring for GUI"""
	def __init__(self, dim):

		self.game_dim = dim

		self.P1_PAD = 20
		self.P1_HT = self.P1_PAD*2 + 20*12
		self.P1_WD = self.P1_PAD*2 + 200

		self.P2_PAD = 20
		self.P2_HT = self.P2_PAD*2 + 40*dim[0] - 40
		self.P2_WD = self.P2_PAD*2 + 40*dim[1] - 40

		self.P3_PAD = 20
		self.P3_HT = self.P3_PAD*2 + 20
		self.P3_WD = self.P3_PAD*2 + 600

		self.P1_COOD_0 = self.P1_PAD + max(0, self.P2_HT - self.P1_HT)/2.0
		self.P1_COOD_1 = self.P1_PAD + max(0, self.P3_WD - self.P1_WD - self.P2_WD)/2.0

		self.P2_COOD_0 = self.P2_PAD + max(0, self.P1_HT - self.P2_HT)/2.0
		self.P2_COOD_1 = self.P2_PAD + self.P1_WD + max(0, self.P3_WD - self.P1_WD - self.P2_WD)/2.0

		self.P3_COOD_0 = self.P3_PAD + max(self.P1_HT, self.P2_HT)
		self.P3_COOD_1 = self.P3_PAD + max(0, self.P1_WD + self.P2_WD - self.P3_WD)/2.0

		self.WINDOW_HT = max(self.P1_HT, self.P2_HT) + self.P3_HT
		self.WINDOW_WD = max(self.P1_WD + self.P2_WD, self.P3_WD)

		turtle.title("Align three")
		turtle.setup(width=self.WINDOW_WD, height=self.WINDOW_HT)
		turtle.setworldcoordinates(0, self.WINDOW_HT, self.WINDOW_WD, 0)

		turtle.ht()
		turtle.pu()
		turtle.speed(0)
		turtle.delay(0)