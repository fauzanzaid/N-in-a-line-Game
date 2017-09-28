#! /usr/bin/python2

import threading
import time
import sys

from state import State
from game import Game
from ctrlrManual import ControllerManual
from ctrlrMinMax import ControllerMinMax
from ctrlrMinMaxAlphaBeta import ControllerMinMaxAlphaBeta


class Main(threading.Thread):
	"""docstring for Main"""

	KEY_DRAW_GRID = "1"
	KEY_PLAY_MM = "2"
	KEY_PLAY_AB = "3"
	KEY_DISP_RES = "4"
	KEY_PLAY_H = "5"
	KEY_QUIT = "q"
	KEY_END = "e"

	INFO_HELP =	(
	"(1) Display board            (4) Calculate Statistics\n"
	"(2) Play against Minimax     (5) Play against human\n"
	"(3) Play against AlphaBeta   (q) Quit (anytime)\n")
	INFO_INIT = "Welcome to Align Three! Press a key ...\n"+INFO_HELP
	INFO_DRAW = "Game drawn!\n"+INFO_HELP
	INFO_WIN_A = "Player M Won! Player H Lost!\n"+INFO_HELP
	INFO_WIN_B = "Player H Won! Player M Lost!\n"+INFO_HELP
	INFO_GAME_MM = "Playing against Minimax\n(q) to quit"
	INFO_GAME_AB = "Playing against AlphaBeta\n(q) to quit"
	INFO_GAME_H = "Playing against Human\n(q) to quit"


	def __init__(self, dim, min_length, qu_usr_ip, qu_cmd):
		super(Main, self).__init__()
		self.time_init = time.time()

		self.game_dim = dim
		self.min_length = min_length
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd


	def play(self, cont_A, cont_B):
		self.send_cmd("clear_grid")
		game = Game(self.game_dim, self.min_length, cont_A, cont_B)
		game.on_move_success = self.send_cmd_draw_move
		res = game.run()

		if res == Game.GAME_WIN_A:
			self.send_cmd("display_info", self.INFO_WIN_A)
		elif res == Game.GAME_WIN_B:
			self.send_cmd("display_info", self.INFO_WIN_B)
		else:
			self.send_cmd("display_info", self.INFO_DRAW)


	def send_cmd_draw_move(self, state, move):
		self.send_cmd("draw_move", move)


	def send_cmd(self, cmd, *args):
		msg = (cmd, args)
		self.qu_cmd.put(msg)


	def print_move_failure(self, state, move):
		print "Play again!", move, "not in", State.move_positions(state)


	def get_pos(self, state):
		while True:
			usr_ip = self.qu_usr_ip.get()
			time, dev, arg = usr_ip
			# print "Main rcvd", usr_ip
			if dev == "mouse":
				return arg
			elif arg == self.KEY_QUIT:
				self.send_cmd("quit")
				sys.exit(0)


	def play_MM(self):
		self.send_cmd("display_info", self.INFO_GAME_MM)
		cont_A = ControllerMinMax("MM", State.PLAYER_A)
		cont_B = ControllerManual("H", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)


	def play_AB(self):
		self.send_cmd("display_info", self.INFO_GAME_AB)
		cont_A = ControllerMinMaxAlphaBeta("AB", State.PLAYER_A)
		cont_B = ControllerManual("H", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)


	def play_H(self):
		self.send_cmd("display_info", self.INFO_GAME_H)
		cont_A = ControllerManual("HA", State.PLAYER_A, self.get_pos)
		cont_B = ControllerManual("HB", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)


	def run(self):
		self.send_cmd("display_info", self.INFO_INIT)

		while True:
			usr_ip = self.qu_usr_ip.get()
			time, dev, arg = usr_ip
			# print "Main rcvd", usr_ip

			if dev == "mouse":
				continue

			elif arg == self.KEY_QUIT:
				self.send_cmd("quit")
				break

			elif arg == self.KEY_DRAW_GRID:
				self.send_cmd("draw_grid")

			elif arg == self.KEY_PLAY_MM:
				self.play_MM()

			elif arg == self.KEY_PLAY_AB:
				self.play_AB()

			elif arg == self.KEY_PLAY_H:
				self.play_H()

			elif arg == self.KEY_DISP_RES:
				pass
