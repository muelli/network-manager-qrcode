#!/usr/bin/env python

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
