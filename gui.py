#! /usr/bin/python2

import turtle
import threading
import time

from state import State

class GUI(threading.Thread):
	"""docstring for GUI"""

	KEY_DRAW_GRID = "1"
	KEY_PLAY_MM = "2"
	KEY_PLAY_AB = "3"
	KEY_DISP_RES = "4"
	KEY_PLAY_H = "5"
	KEY_QUIT = "q"
	KEY_END = "e"

	def __init__(self, dim, qu_usr_ip, qu_cmd):
		super(GUI, self).__init__()
		
		self.time_init = time.time()

		self.game_dim = dim
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd

		self.TILE_SIZE = 40
		self.COIN_SIZE = 30
		self.COIN_COL_A = (1,0,0)
		self.COIN_COL_B = (0,1,0)
		self.LINE_SPACE = 16

		self.P1_PAD = 20
		self.P1_HT = self.P1_PAD*2 + self.LINE_SPACE*13
		self.P1_WD = self.P1_PAD*2 + 400

		self.P2_PAD = 60
		self.P2_HT = self.P2_PAD*2 + self.TILE_SIZE*(dim[0]-1)
		self.P2_WD = self.P2_PAD*2 + self.TILE_SIZE*(dim[1]-1)

		self.P3_PAD = 20
		self.P3_HT = self.P3_PAD*2 + 70
		self.P3_WD = self.P3_PAD*2 + 400

		self.P1_COOD_X = + self.P1_PAD + max(0, self.P3_WD - self.P1_WD - self.P2_WD)/2.0
		self.P1_COOD_Y = - self.P1_PAD + self.P1_HT + self.P3_HT + max(0, self.P2_HT - self.P1_HT)/2.0

		self.P2_COOD_X = + self.P2_PAD + self.P1_WD + max(0, self.P3_WD - self.P1_WD - self.P2_WD)/2.0
		self.P2_COOD_Y = - self.P2_PAD + self.P2_HT + self.P3_HT + max(0, self.P1_HT - self.P2_HT)/2.0

		self.P3_COOD_X = + self.P3_PAD + max(0, self.P1_WD + self.P2_WD - self.P3_WD)/2.0
		self.P3_COOD_Y = - self.P3_PAD + self.P3_HT

		self.WINDOW_HT = max(self.P1_HT, self.P2_HT) + self.P3_HT
		self.WINDOW_WD = max(self.P1_WD + self.P2_WD, self.P3_WD)
		self.WINDOW_PAD = 20

		self.DISPATCH_DELAY = 1


	def draw_tile(self, cood):
		self.ttl.goto(cood[0]-self.TILE_SIZE/2.0, cood[1]-self.TILE_SIZE/2.0)
		self.ttl.seth(0)
		self.ttl.pd()
		for i in xrange(4):
			self.ttl.fd(self.TILE_SIZE)
			self.ttl.lt(90)
		self.ttl.pu()


	def draw_grid(self):

		old_color = self.ttl.color()

		self.ttl.goto(self.P2_COOD_X - self.P2_PAD, self.P2_COOD_Y + self.P2_PAD)
		self.ttl.seth(0)

		self.ttl.pd()
		self.ttl.color((0.9,0.9,0.9),(1,1,1))
		self.ttl.fd(self.P2_WD)
		self.ttl.rt(90)
		self.ttl.fd(self.P2_HT)
		self.ttl.rt(90)
		self.ttl.fd(self.P2_WD)
		self.ttl.rt(90)
		self.ttl.fd(self.P2_HT)
		self.ttl.pu()

		self.ttl.color(old_color[0], old_color[1])


		for i in xrange(self.game_dim[1]):
			for j in xrange(self.game_dim[0]):
				cood_x = self.P2_COOD_X + i*self.TILE_SIZE
				cood_y = self.P2_COOD_Y - j*self.TILE_SIZE
				self.draw_tile((cood_x, cood_y))


	def draw_move(self, move):
		player, pos = move
		cood_x = self.P2_COOD_X + pos[1]*self.TILE_SIZE
		cood_y = self.P2_COOD_Y - pos[0]*self.TILE_SIZE
		self.ttl.goto(cood_x, cood_y)

		if player == State.PLAYER_A:
			self.ttl.dot(self.COIN_SIZE, self.COIN_COL_A)
		else:
			self.ttl.dot(self.COIN_SIZE, self.COIN_COL_B)


	def clear_grid(self):
		for i in xrange(self.game_dim[1]):
			for j in xrange(self.game_dim[0]):
				cood_x = self.P2_COOD_X + i*self.TILE_SIZE
				cood_y = self.P2_COOD_Y - j*self.TILE_SIZE
				self.ttl.goto(cood_x, cood_y)
				self.ttl.dot(self.COIN_SIZE, (1,1,1))


	def display_info(self, text):
		old_color = self.ttl.color()

		self.ttl.goto(self.P3_COOD_X - self.P3_PAD, self.P3_COOD_Y + self.P3_PAD)
		self.ttl.seth(0)

		self.ttl.pd()
		self.ttl.color((0.9,0.9,0.9),(1,1,1))
		self.ttl.fill(True)
		self.ttl.fd(self.P3_WD)
		self.ttl.rt(90)
		self.ttl.fd(self.P3_HT)
		self.ttl.rt(90)
		self.ttl.fd(self.P3_WD)
		self.ttl.rt(90)
		self.ttl.fd(self.P3_HT)
		self.ttl.fill(False)
		self.ttl.pu()

		self.ttl.color(old_color[0], old_color[1])

		self.ttl.goto(self.P3_COOD_X, self.P3_COOD_Y - self.P3_HT + 2*self.P3_PAD)
		self.ttl.write(text, font=("Mono", 8, "normal"))


	def display_results(self, stats):

		old_color = self.ttl.color()

		self.ttl.goto(self.P1_COOD_X - self.P1_PAD, self.P1_COOD_Y + self.P1_PAD)
		self.ttl.seth(0)

		self.ttl.pd()
		self.ttl.color((0.9,0.9,0.9),(1,1,1))
		self.ttl.fill(True)
		self.ttl.fd(self.P1_WD)
		self.ttl.rt(90)
		self.ttl.fd(self.P1_HT)
		self.ttl.rt(90)
		self.ttl.fd(self.P1_WD)
		self.ttl.rt(90)
		self.ttl.fd(self.P1_HT)
		self.ttl.fill(False)
		self.ttl.pu()

		self.ttl.color(old_color[0], old_color[1])

		for i in xrange(1,14):
			self.ttl.goto(self.P1_COOD_X, self.P1_COOD_Y - i*self.LINE_SPACE)
			self.ttl.write("R"+str(i)+"\t: "+str(stats[i]), font=("Mono", 8, "normal"))


	def cmd_dispatcher(self):
		if self.qu_cmd.empty():
			self.scr.ontimer(self.cmd_dispatcher, self.DISPATCH_DELAY)
			return

		func, args = self.qu_cmd.get()
		if func == "quit":
			self.scr.onclick(None)
			self.scr.onkey(None, self.KEY_DRAW_GRID)
			self.scr.onkey(None, self.KEY_PLAY_MM)
			self.scr.onkey(None, self.KEY_PLAY_AB)
			self.scr.onkey(None, self.KEY_DISP_RES)
			self.scr.onkey(None, self.KEY_PLAY_H)
			self.scr.onkey(None, self.KEY_QUIT)
			self.scr.onkey(None, self.KEY_END)
			self.scr.bye()
			return

		elif func == "draw_grid":
			self.draw_grid()

		elif func == "draw_move":
			self.draw_move(*args)

		elif func == "clear_grid":
			self.clear_grid()

		elif func == "display_info":
			self.display_info(*args)

		elif func == "display_results":
			self.display_results(*args)

		self.scr.ontimer(self.cmd_dispatcher, self.DISPATCH_DELAY)


	def send_mouse_click(self, x, y):
		pos = [-1,-1]

		pos[1] = int(round(float(x-self.P2_COOD_X)/self.TILE_SIZE))
		pos[0] = int(round(float(self.P2_COOD_Y-y)/self.TILE_SIZE))

		msg = (time.time()-self.time_init, "mouse", pos)
		self.qu_usr_ip.put(msg)


	def send_key_press(self, key):
		msg = (time.time()-self.time_init, "keypress", key)
		self.qu_usr_ip.put(msg)


	def run(self):

		self.ttl = turtle.Turtle()
		self.scr = turtle.Screen()

		self.scr.setup(width=self.WINDOW_WD+2*self.WINDOW_PAD, height=self.WINDOW_HT+2*self.WINDOW_PAD)
		self.scr.setworldcoordinates(0-self.WINDOW_PAD, 0-self.WINDOW_PAD, self.WINDOW_WD+self.WINDOW_PAD, self.WINDOW_HT+self.WINDOW_PAD)

		self.scr.title("Align three")

		self.ttl.ht()
		self.ttl.pu()
		self.ttl.speed(0)
		self.scr.delay(0)

		# self.draw_grid()

		self.scr.ontimer(self.cmd_dispatcher, self.DISPATCH_DELAY)
		self.scr.onclick(self.send_mouse_click)
		self.scr.onkey(lambda:self.send_key_press("x"), "x")
		self.scr.onkey(lambda:self.send_key_press(self.KEY_DRAW_GRID), self.KEY_DRAW_GRID)
		self.scr.onkey(lambda:self.send_key_press(self.KEY_PLAY_MM), self.KEY_PLAY_MM)
		self.scr.onkey(lambda:self.send_key_press(self.KEY_PLAY_AB), self.KEY_PLAY_AB)
		self.scr.onkey(lambda:self.send_key_press(self.KEY_PLAY_H), self.KEY_PLAY_H)
		self.scr.onkey(lambda:self.send_key_press(self.KEY_DISP_RES), self.KEY_DISP_RES)
		self.scr.onkey(lambda:self.send_key_press(self.KEY_QUIT), self.KEY_QUIT)
		self.scr.onkey(lambda:self.send_key_press(self.KEY_END), self.KEY_END)
		self.scr.listen()


		turtle.done()
