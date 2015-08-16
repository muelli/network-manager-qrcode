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

from hashlib import md5


class quotedphrase(type("foo")):
    def __str__(self):
        return '"%s"' % super(quotedphrase, self).__str__()

def create_string(connection):
    """A string to be parsed may look like this:
        WIFI:T:WPA;S:trololol;P:"12345678";;
    """
    s_con = connection['connection']
    security = connection['802-11-wireless-security']
    
    ssid = s_con['id']
    
    if 'wep-key0' in security:
        sectype = 'WEP'
        password = security['wep-key0']
        passphrase = quotedphrase(password)
        # Hm, let's assume that it's a 128 bit passphrase
        # http://pygmalion.nitri.de/convert-wep-passphrase-into-hex-75.html
        l = len(password)
        ba = bytearray(64)
        for i in range(64):
            c = "%c" % bytes(password[i % l])
            print "C: %r" % c
            ba[i] = c
        digest = md5(ba)
        WEPSTRONGKEYSIZE = 13
        passphrase = digest.hexdigest()[:26]
    else:
        sectype = 'WPA'
        passphrase = security['psk']

    s  = "WIFI:"
    s += "T:%s;" % sectype
    s += "S:%s;" % ssid
    # When the passphrase can be interpreted as hex, it shold be quoted.
    # We manage that quoting with the quoted phrase class
    #s += "P:\"%s\";" % passphrase
    s += "P:%s;" % passphrase
    s += ";"

    return s


if __name__ == '__main__':
    connection = {
        'config': {
            'id': 'foo',
        },
        '802-11-wireless-security' : {
            'key-mgmt': 'wpa',
            'psk': 'my passphrase',
        },
    }
    print (create_string (connection))
