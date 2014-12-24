#!/usr/bin/python

# whosehom.py
#
# Checks the local network using nmap and illuminates some LEDs based on whose
# devices are currently on the local network
#
# Bobby Reynolds

import config
from frameio import FrameIO
from networkscanner import NetworkScanner
from os import setsid
import signal
from sys import exit
from time import sleep

def int_handler(signum, frame):
    print("caught int")
    fio.stop()
    ns.stop()
    exit(0)

def term_handler(signum, frame):
    print("caught term")
    fio.stop()
    ns.stop()
    exit(0)

signal.signal(signal.SIGINT, int_handler)
signal.signal(signal.SIGTERM, term_handler)

ns = NetworkScanner()
ns.start()

fio = FrameIO(ns)
fio.start()

# Keep main thread alive to catch signals
while True:
	sleep(1)
