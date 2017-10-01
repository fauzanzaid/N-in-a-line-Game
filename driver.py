#! /usr/bin/python2

import Queue

from gui import GUI
from main import Main
from config import Config

qu_usr_ip = Queue.Queue()
qu_cmd = Queue.Queue()

dim = Config.board_dimensions
min_length = Config.minimum_coins_aligned_to_win
first = Config.first
precalc = Config.precalc
rdmz = Config.rdmz

gui = GUI(dim, qu_usr_ip, qu_cmd)
main = Main(dim, min_length, qu_usr_ip, qu_cmd, first, precalc, rdmz)

main.start()
gui.start()

main.join()
gui.join()
