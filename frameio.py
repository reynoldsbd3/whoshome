#!/usr/bin/python

# frameio.py
#
# Module for interacting with a picture frame with lights and a button to show
#   who's on the current network.

import config
import os
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
        self.switch_pin = config.switch_pin
        self.gpio_mode = config.gpio_mode
        self.update_freq = config.update_freq

        self.thread = Thread(target = self.run)
        self.thread.deamon = True

        self.init_gpio()

        self.lights_on = True

    def run(self):
        """Update the light status"""

        switch_held = False

        while self.running:
            self.get_colors()
            self.update_colors()
            if GPIO.input(self.switch_pin):
                if switch_held:
                    os.system('shutdown -hP now')
                    # Flash!
                    while self.running:
                        for color, pin in self.pin_bindings.items():
                            GPIO.output(pin, True)
                        sleep(1)
                        for color, pin in self.pin_bindings.items():
                            GPIO.output(pin, False)
                        sleep(1)
                    break
                else:
                    # Shutdown next time if still held
                    switch_held = True
            sleep(self.update_freq)

    def init_gpio(self):
        """Initialize the GPIO pins"""

        if self.gpio_mode == 'board':
            GPIO.setmode(GPIO.BOARD)
        elif self.gpio_mode == 'bcm':
            GPIO.setmode(GPIO.BCM)

        for color, pin in self.pin_bindings.items():
            GPIO.setup(pin, GPIO.OUT)

        GPIO.setup(self.switch_pin, GPIO.IN)
	GPIO.add_event_detect(self.switch_pin, GPIO.RISING, callback = self.toggle_lights, bouncetime = 200)

    def deinit_gpio(self):
        """Make sure pins are off"""

        for color, pin in self.pin_bindings.items():
            GPIO.output(pin, False)

        GPIO.cleanup()

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
                GPIO.output(self.pin_bindings[color], True)
            else:
                GPIO.output(self.pin_bindings[color], False)

    def toggle_lights(self, pin):
        """Toggle whether or not to light LEDs"""
        print('running callback')
        self.lights_on = not self.lights_on

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.deinit_gpio()
