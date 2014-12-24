#!/usr/bin/python

# whosehome.py
#
# Checks the local network using nmap and illuminates some LEDs based on who's
# devices are currently on the local network
#
# Bobby Reynolds

import config
from frameio import FrameIO
from networkscanner import NetworkScanner
import signal
from time import sleep

def kill_handler(signum, frame):
    print("caught term or int")
    fio.stop()
    ns.stop()

signal.signal(signal.SIGINT, kill_handler)
signal.signal(signal.SIGTERM, kill_handler)

ns = NetworkScanner()
ns.start()

fio = FrameIO(ns)
fio.start()
