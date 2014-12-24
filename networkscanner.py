#!/usr/bin/python

# networkscanner.py
#
# Module for scanning the local network and getting a list of which of the
#   tracked MAC addresses are actually on the same subnet.
#
# Bobby Reynolds

import config
from nmap import PortScanner
from threading import Thread

class NetworkScanner():
    """The network scanner is given a list of MAC addresses and maintains a
        publicly accessible dictionary of those addresses and whether the
        device is on the local network segment."""

    def __init__(self, name = "NetworkScanner"):
        self.name = name

        self.local_net = config.local_net
        self.nmap_args = config.nmap_args
        self.timeout = config.timeout

        # Associate 0 with each MAC
        self.macs = {}
        for mac in config.macs:
            self.macs[mac] = 0

        # Don't need to worry about losing this when the program terminates
        self.thread = Thread(target = self.run)
        self.thread.deamon = True

    def run(self):
        """Scan the network for MAC addresses and keep tabs on which devices
            are present or have left"""

        nm = PortScanner()

        while self.running:

            # Decrement all hosts
            for mac in self.macs:
                if self.macs[mac] > 0:
                    self.macs[mac] -= 1;

            nm.scan(hosts = self.local_net, arguments = self.nmap_args)

            # Mark each host found as present unless it is not tracked
            for host in nm.all_hosts():
                try:
                    mac = nm[host]['addresses']['mac']
                    if mac in self.macs:
                        self.macs[mac] = self.timeout + 1 # Immediately decremented
                except KeyError:
                    # nmap didn't get the MAC?
                    # Just ignore it I guess
                    pass

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

if __name__ == '__main__':
    print('this is not an executable file')
