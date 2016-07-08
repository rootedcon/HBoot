#!/bin/env python
#
# (c) RootedCON 2016
# Authors: Javier Olascoaga <jolascoaga@rootedcon.com>, Román Ramírez <rramirez@rootedcon.com>
#
# Usage: run on boot to get a "sentinel" file, and then check this signature to detect tampering
# of your boot or first disk sectors.
#

import re, os, sys
import hashlib

boot_device = '/dev/sda'
sector_count = 10
backup_file = '/tmp/backup_boot.dat'
SENTINEL_SIGNATURE_FILE = '/etc/sentinel.sig'
ALGORITHM   = 'sha512'

msg = {
        'error': { 'msg': 'SENTINEL-KO', 'code': -1 },
        'ok': { 'msg': 'SENTINEL-OK', 'code': 0 },
}

DEBUG=True

def debug(data):
    if DEBUG:
        print data

def _hash(data):
    m = eval('hashlib.' + ALGORITHM + '()')
    m.update(data)
    return m.hexdigest()

def get_sectors():
    with open(boot_device, 'rb') as f:
        return f.read(10)

def new_run():
    resDump = get_sectors()
    resSignature = _hash(resDump)
    debug("resDumpBlock=[%s] resSignature=[%s]" % (resDump, resSignature))
    try:
        with open(SENTINEL_SIGNATURE_FILE, "w") as f:
            f.write(resSignature)
        return True
    except Exception as e:
        debug("ERROR: %s" % str(e))
        return False

def verify():
    signature = None
    resDump = get_sectors()
    resSignature = _hash(resDump)
    debug("resDumpBlock=[%s] resSignature=[%s]" % (resDump, resSignature))

    try:
        with open(SENTINEL_SIGNATURE_FILE, "rt") as tfile:
            if resSignature == tfile.readline().strip():
                return True
            return False
    except Exception as e:
        debug("ERROR: cannot verify signature: %s"% str(e))
        return False

def run():
    if not os.path.isfile(SENTINEL_SIGNATURE_FILE):
        debug("SENTINEL FILE DOES NOT EXIST")
        return new_run()
    else:
        debug("Sentinel file already exists...")
        if verify() == False:
            print msg['error']['msg']
            return msg['error']['code']
        else:
            print msg['ok']['msg']
            return msg['ok']['code']


if  __name__ == '__main__':
    sys.exit(run())

