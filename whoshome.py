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
from time import sleep

def main():

    ns = NetworkScanner()
    ns.start()

    fio = FrameIO(ns)
    fio.start()

    while 1:
        print('letting scanner do its thing')
        sleep(5)
        print('found this:')
        for mac, active in ns.macs.items():
            if active:
                print('\tfound \'%s\'' % (mac))

if __name__ == '__main__':
    main()
