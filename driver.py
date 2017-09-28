#! /usr/bin/python2

import Queue

from gui import GUI
from main import Main

qu_usr_ip = Queue.Queue()
qu_cmd = Queue.Queue()

dim = (4,4)
min_length = 3

gui = GUI(dim, qu_usr_ip, qu_cmd)
main = Main(dim, min_length, qu_usr_ip, qu_cmd)

main.start()
gui.start()

main.join()
gui.join()
