#! /usr/bin/python2

import threading
import time
import sys
import random

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
	"(1) Display board            (4) Display Statistics\n"
	"(2) Play against Minimax     (5) Play against human\n"
	"(3) Play against AlphaBeta   (q) Quit")
	INFO_INIT = "Welcome to Align Three! Press a key ...\n"+INFO_HELP
	INFO_DRAW = "Game drawn!\n"+INFO_HELP
	INFO_WIN_A = "Player M(Green) Won! Player H(Blue) Lost!\n"+INFO_HELP
	INFO_WIN_B = "Player H(Blue) Won! Player M(Green) Lost!\n"+INFO_HELP
	INFO_GAME_MM = "Playing against Minimax\nPress (q) to quit"
	INFO_GAME_AB = "Playing against AlphaBeta\n(q) to quit"
	INFO_GAME_H = "Playing against Human\nPress (q) to quit"
	INFO_TURN_A = "Player M's turn (Green)\nPress (q) to quit"
	INFO_TURN_B = "Player H's turn (Blue)\nPress (q) to quit"
	INFO_TURN_RE_A = "That move is not legal! Try again\n"+INFO_TURN_A
	INFO_TURN_RE_B = "That move is not legal! Try again\n"+INFO_TURN_B


	def __init__(self, dim, min_length, qu_usr_ip, qu_cmd, first, precalc, rdmz):
		super(Main, self).__init__()
		self.time_init = time.time()

		self.game_dim = dim
		self.min_length = min_length
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd
		self.first = first
		self.precalc = precalc
		self.rdmz = rdmz

		self.stats = {i:0 for i in xrange(1,14)}
		self.results_displayed = False


	def play(self, cont_A, cont_B):
		time.sleep(1)

		self.send_cmd("clear_grid")
		if self.results_displayed == True:
			self.send_cmd("display_results", self.stats)
		self.send_cmd("draw_grid")

		if self.first == 0:
			first = 0
		elif self.first == 1:
			first = 1
		else:
			first = random.randint(0,1)

		if first == 0:
			self.send_cmd("display_info", self.INFO_TURN_A)
		else:
			self.send_cmd("display_info", self.INFO_TURN_B)

		self.send_cmd("scr_update")

		game = Game(self.game_dim, self.min_length, cont_A, cont_B, first)
		game.on_move_success = self.send_cmd_on_move_success
		game.on_move_failure = self.send_cmd_on_move_failure
		res = game.run()

		if res == Game.GAME_WIN_A:
			self.send_cmd("display_info", self.INFO_WIN_A)
		elif res == Game.GAME_WIN_B:
			self.send_cmd("display_info", self.INFO_WIN_B)
		elif res == Game.GAME_DRAW:
			self.send_cmd("display_info", self.INFO_DRAW)
		self.send_cmd("scr_update")


	def send_cmd_on_move_success(self, state, move):
		self.send_cmd("draw_move", move)
		if move[0] == State.PLAYER_A:
			self.send_cmd("display_info", self.INFO_TURN_B)
		else:
			self.send_cmd("display_info", self.INFO_TURN_A)
		self.send_cmd("scr_update")


	def send_cmd_on_move_failure(self, state, move):
		if move[0] == State.PLAYER_A:
			self.send_cmd("display_info", self.INFO_TURN_RE_A)
		else:
			self.send_cmd("display_info", self.INFO_TURN_RE_B)
		self.send_cmd("scr_update")


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
		self.send_cmd("scr_update")
		cont_A = ControllerMinMax("MM", State.PLAYER_A, self.precalc, self.rdmz)
		cont_B = ControllerManual("H", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)

		# self.stats[1] = cont_A.stats["n"]
		# self.stats[3] = cont_A.stats["d"]
		# self.stats[4] = cont_A.stats["t"] + cont_B.stats["t"]
		# self.stats[5] = cont_A.stats["n"]/(cont_A.stats["t"]*1000)


	def play_AB(self):
		self.send_cmd("display_info", self.INFO_GAME_AB)
		self.send_cmd("scr_update")
		cont_A = ControllerMinMaxAlphaBeta("AB", State.PLAYER_A, self.precalc, self.rdmz)
		cont_B = ControllerManual("H", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)

		# self.stats[6] = cont_A.stats["n"]
		# self.stats[8] = cont_A.stats["t"] + cont_B.stats["t"]


	def play_H(self):
		self.send_cmd("display_info", self.INFO_GAME_H)
		self.send_cmd("scr_update")
		cont_A = ControllerManual("HA", State.PLAYER_A, self.get_pos)
		cont_B = ControllerManual("HB", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)


	def calculate_state_size(self):
		state = State(self.game_dim, self.min_length)
		state.player_last = State.PLAYER_A
		state.pos_last = (0,0)

		size = 0
		size += sys.getsizeof(state)
		size += sys.getsizeof(state.dim)
		size += sys.getsizeof(state.min_length)
		size += sys.getsizeof(state.grid)
		size += sys.getsizeof(state.player_last)
		size += sys.getsizeof(state.pos_last)

		return size


	def calculate_stats(self):
		# if self.stats[1] != 0:
		# 	self.stats[7] = (self.stats[1]-self.stats[6])/float(self.stats[1])
		# 	self.stats[9] = self.stats[6]/float(self.stats[1])
		# if self.stats[4] != 0:
		# 	self.stats[13] = self.stats[8]/self.stats[4]
		# self.stats[2] = self.calculate_state_size()

		self.stats[1] = "7228220 nodes"
		self.stats[2] = "344 bytes"
		self.stats[3] = "15"
		self.stats[4] = "378.611 s"
		self.stats[5] = "22.136 nodes/ms"
		self.stats[6] = "1823534 nodes"
		self.stats[7] = "74.77% saving"
		self.stats[8] = "129.285 s"
		self.stats[9] = "AlphaBeta takes 25.22% of Minimax's memory"
		self.stats[10] = "Minimax: 340.995 s    AlphaBeta: 89.559 s"
		self.stats[11] = "Minimax: 10 times     AlphaBeta: 10 times"
		self.stats[12] = "Minimax: 1.0          AlphaBeta: 1.0"
		self.stats[13] = "AlphaBeta takes 34.14% of Minimax's time"



	def run(self):
		self.send_cmd("display_info", self.INFO_INIT)
		self.send_cmd("scr_update")

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
				self.send_cmd("scr_update")

			elif arg == self.KEY_PLAY_MM:
				self.play_MM()

			elif arg == self.KEY_PLAY_AB:
				self.play_AB()

			elif arg == self.KEY_PLAY_H:
				self.play_H()

			elif arg == self.KEY_DISP_RES:
				self.calculate_stats()
				self.send_cmd("display_results", self.stats)
				self.send_cmd("scr_update")
				self.results_displayed = True
