#!/usr/bin/python

# frameio.py
#
# Module for interacting with a picture frame with lights and a button to show
#   who's on the current network.

import config
from RPi import GPIO
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
        self.gpio_mode = config.gpio_mode
        self.update_freq = config.update_freq

        self.thread = Thread(target = self.run)
        self.thread.deamon = True

        self.init_gpio()

    def run(self):
        """Update the light status"""

        while self.running:
            self.get_colors()
            self.update_colors()
            sleep(self.update_freq)

    def init_gpio(self):
        """Initialize the GPIO pins"""

        if self.gpio_mode == 'board':
            GPIO.setmode(GPIO.BOARD)
        elif self.gpio_mode == 'bcm':
            GPIO.setmode(GPIO.BCM)

        for color, pin in self.pin_bindings.items():
            GPIO.setup(pin, GPIO.OUT)

    def deinit_gpio(self):
        """Make sure pins are off"""

        for color, pin in self.pin_bindings.items():
            GPIO.output(pin, False)

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
            if lit:
                GPIO.output(pin_bindings[color], True)
            else:
                GPIO.output(pin_bindings[color], False)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.deinit_gpio()
