#!/usr/bin/env python

# config.py
#
# Simple python syntax variable assignments used to configure the whoshome
#   application.
#
# Bobby Reynolds

# MAC addresses to search for. The provided colors should be one in the list of
#   colors specified later in this file. These should be of the form
#   'MAC' : 'color'
macs = {'DC:F1:10:B6:69:84' : 'blue',
        '74:D4:35:02:9C:26' : 'red',
        '94:94:26:22:AA:69' : 'green'}

# Address/netmask for the local subnet to scan. If your local network uses a
#   different subnet, change this so that nmap scans the proper addresses.
local_net = '192.168.1.1/24'

# Number of consecutive scans that a device must be absent from to be considered
#   gone from the local network
timeout = 8

# Args to pass to nmap... shouldn't need to change these
nmap_args = '-sn -n --host-timeout 4s'

# Colors and GPIO configuration. Also shouldn't change these unless you have a
#   different hardware configuration. These should be of the form 'color' : pin
colors = {'red' : 4,
          'yellow' : 17,
          'green' : 22,
          'blue' : 5}

# Pin to be used as switch input
switch_pin = 25

# Number of seconds between output updates
update_freq = 3

# Numbering mode for GPIO pins
gpio_mode = 'bcm'

if __name__ == '__main__':
    print('this is not an executable file')
