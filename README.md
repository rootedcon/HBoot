# HBoot
Script to extract a signature of the first blocks of the disk, to be able to dectect boot tampering attemps.


## Why:
- Because we are paranoid about boot hijacking. So thinking about the easiest way to be able to detect tampering attemps...
this is the result.

## Who:

- Javier Olascoaga <jolascoaga@rootedcon.com>
- Román Ramírez <rramirez@rootedcon.com>

https://www.rootedcon.com

## How to:

Put this script onto your init scripts (quick-dirty /etc/rc.local) and whenever you get SENTINEL-KO and/or $? == -1,
you can raise an alarm.

We use to change the desktop background to red (i.e, if you use gnome and have a red.jpg image with is, well, this, red, 
gsettings set org.gnome.desktop.background picture-uri file:///tmp/red.jpg), show a warning window through zenity
(i.e, zenity  --error --text="WARNING TEXT") or do the action you consider.

## Customize:

### boot_device = '/dev/sda'

The device you want to read block from.

### sector_count = 10

The number of blocks you want to read.

### backup_file = '/tmp/backup_boot.dat'

The temporal backup file to get the hash.

### SENTINEL_SIGNATURE_FILE = '/etc/sentinel.sig'

The sentinel file where to store the hash result to be compared on every boot.

### ALGORITHM   = 'sha512'

The algorithm you want to use. Please, remember that not every openssl implementation includes all the hashing algorithms.
If you want to check in your specific platform for which ones are available:

- openssl dgst -help
- python -c 'import hashlib;print hashlib.algorithms'
- over 2.7.9, python -c 'import hashlib;print hashlib.algorithms_available'

### Messages:

"msg", is the text to be printed on screen and "code" is the return code you can test with $?

msg = {
        'error': { 'msg': 'SENTINEL-KO', 'code': -1 },
        'ok': { 'msg': 'SENTINEL-OK', 'code': 0 },
}


Happy hacking!
