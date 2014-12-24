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
        '52:54:00:7C:EC:E1' : 'red'}

# Address/netmask for the local subnet to scan. If your local network uses a
#   different subnet, change this so that nmap scans the proper addresses.
local_net = '10.128.1.1/16'

# Number of consecutive scans that a device must be absent from to be considered
#   gone from the local network
timeout = 10

# Args to pass to nmap... shouldn't need to change these
nmap_args = '-sn -n --host-timeout 2s'

# Colors and GPIO configuration. Also shouldn't change these unless you have a
#   different hardware configuration. These should be of the form 'color' : pin
colors = {'blue' : 0,
          'red' : 1,
          'yellow' : 2}

# Number of seconds between output updates
update_freq = 3

if __name__ == '__main__':
    print('this is not an executable file')
