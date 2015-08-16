#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2015 Tobias Mueller <muelli@cryptobitch.de>
#
import sys

import pyqrcode

from read_connections import list_connections
from create_barcode_string import create_string
from get_active_connections import get_active_connections

def barcode_from_connection(connection):
    s = create_string(connection)
    barcode = pyqrcode.create(s)
    return barcode



if __name__ == '__main__':
    import textwrap
    connections = list_connections()
    if len(sys.argv) == 1:
        for i, c in enumerate(connections):
            print ("%5d: %s" % (i, c['connection']['id']))
        print ()
        connection = next(get_active_connections())
        print ("Using active connection %s", connection)
    else:
        selection = int(sys.argv[1])
        print ("Selecting %d" % selection)
        connection = connections[selection]
    
    key = connection['802-11-wireless-security'].get('psk', None) or \
          connection['802-11-wireless-security']['wep-key0']
    
    print ("%s - %s" % (connection['connection']['id'], key))
    s = barcode_from_connection(connection)
    print ("String: %s" % s.data)
    print ("%s" % s.terminal(quiet_zone=1,
                    module_color='black', background='white'
                    ))
    #s.svg('/tmp/barcode.svg')
    #s.eps('/tmp/barcode.epg')
    #s.png('/tmp/barcode.png')
