#!/usr/bin/python

# frameio.py
#
# Module for interacting with a picture frame with lights and a button to show
#   who's on the current network.

import config
#import RPi.GPIO as GPIO
from threading import Thread
from time import sleep

class FrameIO():
    """The FrameIO object runs on a loop checking the network scanner and
        updating the output lights. It also deals with the input button which
        toggles the lights."""

    def __init__(self, networkscanner):
        self.networkscanner = networkscanner

        self.macs = config.macs
        self.colors = {}
        for color in config.colors:
            self.colors[color] = False # All lights start off
        self.pin_bindings = config.colors
        self.update_freq = config.update_freq

        self.thread = Thread(target = self.run)
        self.thread.deamon = True

        # Set an event handler for the off button
        self.lights_on = True
        #GPIO.something(target = self.light_switch)

        # Prepare GPIO pins for output
        self.setup_pins()

    def run(self):
        """Update the light status"""

        while 1:
            self.get_colors()
            self.update_colors()
            sleep(self.update_freq)

    def light_switch(self):
        """Toggle whether or not the lights should be lit"""
        self.lights_on = False

    def setup_pins(self):
        """Setup GPIO pins for input and output"""
        pass

    def get_colors(self):
        """Update which colors should be lit based on networkscanner"""

        # First assume all are off
        for color in self.colors:
            self.colors[color] = False

        # Now set colors to on if there is a device present
        for mac, present in self.networkscanner.macs.items():
            if present:
                self.colors[self.macs[mac]] = True

    def update_colors(self):
        """Do the work of lighting the actual pins"""

        for color, lit in self.colors.items():
            if lit and self.lights_on:
                print('lighting pin %s' % (self.pin_bindings[color]))
            else:
                print('turning off pin %s' % (self.pin_bindings[color]))

    def start(self):
        self.thread.start()
