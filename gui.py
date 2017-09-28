#! /usr/bin/python2

import turtle

from state import State

class GUI(object):
	"""docstring for GUI"""
	def __init__(self, dim):

		self.game_dim = dim

		self.TILE_SIZE = 40
		self.COIN_SIZE = 30
		self.COIN_COL_A = (1,0,0)
		self.COIN_COL_B = (0,1,0)

		self.P1_PAD = 20
		self.P1_HT = self.P1_PAD*2 + 20*12
		self.P1_WD = self.P1_PAD*2 + 200

		self.P2_PAD = 20
		self.P2_HT = self.P2_PAD*2 + self.TILE_SIZE*(dim[0]-1)
		self.P2_WD = self.P2_PAD*2 + self.TILE_SIZE*(dim[1]-1)

		self.P3_PAD = 20
		self.P3_HT = self.P3_PAD*2 + 20
		self.P3_WD = self.P3_PAD*2 + 600

		self.P1_COOD_X = + self.P1_PAD + max(0, self.P3_WD - self.P1_WD - self.P2_WD)/2.0
		self.P1_COOD_Y = - self.P1_PAD + self.P1_HT + self.P3_HT + max(0, self.P2_HT - self.P1_HT)/2.0

		self.P2_COOD_X = + self.P2_PAD + self.P1_WD + max(0, self.P3_WD - self.P1_WD - self.P2_WD)/2.0
		self.P2_COOD_Y = - self.P2_PAD + self.P2_HT + self.P3_HT + max(0, self.P1_HT - self.P2_HT)/2.0

		self.P3_COOD_X = + self.P3_PAD + max(0, self.P1_WD + self.P2_WD - self.P3_WD)/2.0
		self.P3_COOD_Y = - self.P3_PAD + self.P3_HT

		self.WINDOW_HT = max(self.P1_HT, self.P2_HT) + self.P3_HT
		self.WINDOW_WD = max(self.P1_WD + self.P2_WD, self.P3_WD)

		turtle.title("Align three")
		turtle.setup(width=self.WINDOW_WD, height=self.WINDOW_HT)
		turtle.setworldcoordinates(0, 0, self.WINDOW_WD, self.WINDOW_HT)

		turtle.ht()
		turtle.pu()
		turtle.speed(0)
		turtle.delay(0)


	def draw_tile(self, cood):
		turtle.goto(cood[0]-self.TILE_SIZE/2.0, cood[1]-self.TILE_SIZE/2.0)
		turtle.seth(0)
		turtle.pd()
		for i in xrange(4):
			turtle.fd(self.TILE_SIZE)
			turtle.lt(90)
		turtle.pu()


	def draw_grid(self):
		for i in xrange(self.game_dim[1]):
			for j in xrange(self.game_dim[0]):
				cood_x = self.P2_COOD_X + i*self.TILE_SIZE
				cood_y = self.P2_COOD_Y - j*self.TILE_SIZE
				self.draw_tile((cood_x, cood_y))


	def draw_move(self, move):
		player, pos = move
		cood_x = self.P2_COOD_X + pos[1]*self.TILE_SIZE
		cood_y = self.P2_COOD_Y - pos[0]*self.TILE_SIZE
		turtle.goto(cood_x, cood_y)

		if player == State.PLAYER_A:
			turtle.dot(self.COIN_SIZE, self.COIN_COL_A)
		else:
			turtle.dot(self.COIN_SIZE, self.COIN_COL_B)


	def clear_grid(self):
		for i in xrange(self.game_dim[1]):
			for j in xrange(self.game_dim[0]):
				cood_x = self.P2_COOD_X + i*self.TILE_SIZE
				cood_y = self.P2_COOD_Y - j*self.TILE_SIZE
				turtle.goto(cood_x, cood_y)
				turtle.dot(self.COIN_SIZE, (1,1,1))
