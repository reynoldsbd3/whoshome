#!/usr/bin/python

# framelights.py
#
# Abstraction layer for LED output
#
# Bobby Reynolds

import config
#import RPi.GPIO as GPIO

class FrameLights():
    """Abstraction class representing some different LEDs with on/off
        functionality"""

    def __init__(self):
        self.colors = config.colors

        # Set up GPIO output
        #GPIO.setmode(GPIO.BOARD)
        for color, pin in self.colors.items():
            #GPIO.setup(pin, GPIO.OUT)
            #GPIO.output(pin, False)
            pass

    def led_on(self, color):
        """Illuminate the corresponding LED"""

        if color in self.colors:
            #GPIO.output(self.colors[color], True)
            print('color \'%s\' turned on' % (color))
        else:
            print('color \'%s\' not recognized' % (color))

    def led_off(self, color):
        """Turn off the corresponding LED"""

        if color in self.colors:
            #GPIO.output(self.colors[color], False)
            print('color \'%s\' turned off' % (color))
        else:
            print('color \'%s\' not recognized' % (color))
