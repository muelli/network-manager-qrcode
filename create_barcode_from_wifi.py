#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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
import json
import logging
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
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    connections = list_connections()
    if len(sys.argv) == 1:
        for i, c in enumerate(connections):
            print(("%5d: %s" % (i, c['connection']['id'])))
        print ()
        connection = next(get_active_connections())
        print("Using active connection")
        log.debug("Connection: %s", connection)
    else:
        selection = int(sys.argv[1])
        print(("Selecting %d" % selection))
        connection = connections[selection]

    try:
        key = connection['802-11-wireless-security'].get('psk', None) or \
              connection['802-11-wireless-security']['wep-key0']
    except KeyError:
        log.exception("Could not find psk nor wep-key0 in keys: %s",
            connection['802-11-wireless-security'].keys())
        log.info("Connection: %s", json.dumps(connection, indent=4))
        raise

    s = barcode_from_connection(connection)
    log.info(("String: %s", s.data))
    print(("%s" % s.terminal(quiet_zone=1,
                    module_color='black', background='white'
                    )))
    print(("%s - %s") % (bytes(connection['802-11-wireless']['ssid']).decode('ascii'), key))
    #s.svg('/tmp/barcode.svg')
    #s.eps('/tmp/barcode.epg')
    #s.png('/tmp/barcode.png')
