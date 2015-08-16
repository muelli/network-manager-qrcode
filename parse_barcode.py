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

import logging


def parse(s):
    '''
    Parses a string for wifi connection settings.
    Refer to https://github.com/zxing/zxing/wiki/Barcode-Contents
    for the format.
    
    A string to be parsed may look like this:
    WIFI:T:WPA;S:trololol;P:"12345678";;
    
    This function would return
    {
        'T':'WPA',
        'S':'trololol',
        'P':'12345678',
    }
    '''
    
    if not s.startswith('WIFI:'):
        logging.info("String does not start with 'WIFI:': %s", s)
    elif not s.endswith(';;'):
        logging.info("String does not end with ';;': %s", s)
    else:
        s = s[len('WIFI:'):-len(';')]
        logging.info('Parsing %s', s)
        
        def parse_key(s, accu=None):
            logging.info('Parsing key from %s', s)
            accu = accu or ''
            key = s[0]
            logging.debug('key: %s', key)
            sep = s[1]
            logging.debug('sep: %s (%s)', sep, sep==':')
            if not sep == ':':
                raise ValueError('Expected :  got %s (%s)' % (sep, s))
            accu += s[2:]
            
            logging.info('Returning key %s (%s)', key, accu)
            return key, accu


        def parse_value(s, accu=None):
            accu = accu or ''
            state = "CHARS"
            v = ''
            for i, c in enumerate(s):
                if c == '"':
                    if state == "CHARS":
                        state = "OPEN_PAREN"
                    elif state == "OPEN_PAREN":
                        state = "CLOSED_PAREN"
                        # So we've finished reading a "protected" string
                        # We don't need to do anything with it, I guess
                    else:
                        raise ValueError("Read Paren in state %s "
                            "but expected either ; or char" % state)
                elif c == ';':
                    # So we've finished reading a string
                    # If we had a paren open, the string is
                    # good as is.  But if we had a paren open,
                    # the string *could* be interpreted as
                    # base16 encoded binary.
                    if not state == 'CLOSED_PAREN':
                        try:
                            decoded = v.decode('hex')
                            logging.info('Interpreting string %s as binary', v)
                            v = decoded
                        except TypeError:
                            logging.debug('String does not want to be hex',
                                exc_info=True)

                    state = 'BREAK'
                    break
                else:
                    if state == "CLOSED_PAREN":
                        raise ValueError("Read char %s after "
                            "a closing paren. Expected ; (%s)" % (c, s))
                    elif state == 'OPEN_PAREN':
                        # We need to read the string such that it is *not* a
                        # hexademical string, but real text
                        v += c
                    else:
                        v += c

            
            if not state == 'BREAK':
                raise ValueError('Finished in state %s. Expected BREAK (%s)', state, s)

            value = v
            i += 1
            accu = s[i:]
            
            logging.debug('Returning value %s (%s)', value, accu)
            return value, accu
        

        def parse_key_value(s):
            key, accu = parse_key(s)
            value, accu = parse_value(accu)
            return key, value, accu
    
    d = {}
    accu = s
    while accu:
        key, value, accu = parse_key_value(accu)
        d[key] = value
    
    return d

            
        

if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    args = sys.argv[1:]
    if len(args) == 0:
        s = 'WIFI:T:WPA;S:trololol;P:"12345678";;'
    else:
        s = args[0]
    parsed = parse(s)
    print(parsed)
