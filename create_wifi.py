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
# Copyright (C) 2011 Red Hat, Inc.
# Copyright (C) 2015 Tobias Mueller <muelli@cryptobitch.de>
#

import dbus
from uuid import uuid4 as uuid


def dict_to_dbus(d):
    "Apparently, we don't need to convert ourselves, so this simply retunrs"
    return d

def build_network_manager_connection_settings(
    ssid=None, key_mgnt='wpa-psk', passwd=None,
    settings={}):
    """Build a dict suitable for handing over to NetworkManager's
    DBus interface for creation of a new connection.
    """

    connection = settings.get('connection', {})
    wireless = settings.get('802-11-wireless', {})
    wireless_security = settings.get('802-11-wireless-security', {})
    enterprise = settings.get('802-1x', {})
    ipv4 = settings.get('ipv4', {})
    ipv6 = settings.get('ipv6', {})


    if not ssid:
        ssid = wireless['ssid']

    connection_defaults = {
        'type': '802-11-wireless',
        'uuid': str(uuid()),
        'id': '%s-from-barcode' % ssid,
    }

    wireless_defaults = {
        'ssid': dbus.ByteArray(ssid),
        #'security': '802-11-wireless'})
        #'security': '802-11-wireless-security',
    }

    if key_mgnt != 'none' and not passwd:
        passwd = wireless_security['psk']

    wireless_security_defaults = {
        'key-mgmt': key_mgnt,
        'psk':  passwd,
    }

    s_8021x = { #dbus.Dictionary({
        #'eap': [],
        #'identity': 'wtf',
        #'client-cert': path_to_value("/some/place/client.pem"),
        #'ca-cert': path_to_value("/some/place/ca-cert.pem"),
        #'private-key': path_to_value("/some/place/privkey.pem"),
    #    'private-key-password': "12345testing"})
    }

    ipv4_defaults = {'method': 'auto'}
    ipv6_defaults = {'method': 'ignore'}


    defaults = {
        'connection': connection_defaults,
        '802-11-wireless': wireless_defaults,
        '802-11-wireless-security': wireless_security_defaults,
        #'802-1x': s_8021x,
        'ipv4': ipv4_defaults,
        'ipv6': ipv6_defaults,
    }
    

    merged_settings = dict(defaults)
    merged_settings['connection'].update(connection)
    merged_settings['802-11-wireless'].update(wireless)
    merged_settings['802-11-wireless-security'].update(wireless_security)
    if key_mgnt == "eap":
        merged_settings['802-1x'].update(enterprise)
    merged_settings['ipv4'].update(ipv4)
    merged_settings['ipv6'].update(ipv6)
    
    return dict_to_dbus(merged_settings)



def submit(connection_settings):
    bus = dbus.SystemBus()
    
    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
    
    return settings.AddConnection(connection_settings)


if __name__ == '__main__':
    settings = build_network_manager_connection_settings(ssid="foo", passwd="bar"*3)
    print(settings)
    print(submit(settings))
