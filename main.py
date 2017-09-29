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
	"(1) Display board            (4) Calculate Statistics\n"
	"(2) Play against Minimax     (5) Play against human\n"
	"(3) Play against AlphaBeta   (q) Quit")
	INFO_INIT = "Welcome to Align Three! Press a key ...\n"+INFO_HELP
	INFO_DRAW = "Game drawn!\n"+INFO_HELP
	INFO_WIN_A = "Player M(Red) Won! Player H(Green) Lost!\n"+INFO_HELP
	INFO_WIN_B = "Player H(Green) Won! Player M(Red) Lost!\n"+INFO_HELP
	INFO_GAME_MM = "Playing against Minimax\nPress (q) to quit"
	INFO_GAME_AB = "Playing against AlphaBeta\n(q) to quit"
	INFO_GAME_H = "Playing against Human\nPress (q) to quit"
	INFO_TURN_A = "Player M's turn (Red)\nPress (q) to quit"
	INFO_TURN_B = "Player H's turn (Green)\nPress (q) to quit"
	INFO_TURN_RE_A = "That move is not legal! Try again\n"+INFO_TURN_A
	INFO_TURN_RE_B = "That move is not legal! Try again\n"+INFO_TURN_B


	def __init__(self, dim, min_length, qu_usr_ip, qu_cmd, first):
		super(Main, self).__init__()
		self.time_init = time.time()

		self.game_dim = dim
		self.min_length = min_length
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd
		self.first = first

		self.stats = {i:0 for i in xrange(1,14)}


	def play(self, cont_A, cont_B):
		self.send_cmd("clear_grid")

		if self.first == 0:
			first = 0
		elif self.first == 1:
			first = 1
		else:
			first = random.randint(0,1)

		time.sleep(1)

		if first == 0:
			self.send_cmd("display_info", self.INFO_TURN_A)
		else:
			self.send_cmd("display_info", self.INFO_TURN_B)

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


	def send_cmd_on_move_success(self, state, move):
		self.send_cmd("draw_move", move)
		if move[0] == State.PLAYER_A:
			self.send_cmd("display_info", self.INFO_TURN_B)
		else:
			self.send_cmd("display_info", self.INFO_TURN_A)


	def send_cmd_on_move_failure(self, state, move):
		if move[0] == State.PLAYER_A:
			self.send_cmd("display_info", self.INFO_TURN_RE_A)
		else:
			self.send_cmd("display_info", self.INFO_TURN_RE_B)


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
			elif arg == self.KEY_DRAW_GRID:
				self.send_cmd("draw_grid")
			elif arg == self.KEY_QUIT:
				self.send_cmd("quit")
				sys.exit(0)


	def play_MM(self):
		self.send_cmd("display_info", self.INFO_GAME_MM)
		cont_A = ControllerMinMax("MM", State.PLAYER_A)
		cont_B = ControllerManual("H", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)

		self.stats[1] = cont_A.stats["n"]
		self.stats[3] = cont_A.stats["d"]
		self.stats[4] = cont_A.stats["t"] + cont_B.stats["t"]
		self.stats[5] = cont_A.stats["n"]/(cont_A.stats["t"]*1000)



	def play_AB(self):
		self.send_cmd("display_info", self.INFO_GAME_AB)
		cont_A = ControllerMinMaxAlphaBeta("AB", State.PLAYER_A)
		cont_B = ControllerManual("H", State.PLAYER_B, self.get_pos)
		self.play(cont_A, cont_B)

		self.stats[6] = cont_A.stats["n"]
		self.stats[8] = cont_A.stats["t"] + cont_B.stats["t"]


	def play_H(self):
		self.send_cmd("display_info", self.INFO_GAME_H)
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
		if self.stats[1] != 0:
			self.stats[7] = (self.stats[1]-self.stats[6])/float(self.stats[1])
			self.stats[9] = self.stats[6]/float(self.stats[1])
		if self.stats[4] != 0:
			self.stats[13] = self.stats[8]/self.stats[4]
		self.stats[2] = self.calculate_state_size()


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
				self.calculate_stats()
				self.send_cmd("display_results", self.stats)
