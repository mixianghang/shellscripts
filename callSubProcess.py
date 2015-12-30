#!/usr/bin/python
import sys
from subprocess import call
call("./testShell.sh {0} {1}".format(sys.argv[1], sys.argv[2]), shell=True)
call("du -hs ./*", shell=True)
