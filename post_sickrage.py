#!/usr/bin/python

import sys

with open('/downloads/process/poll/%s.postprocess' % (sys.argv[3],), 'w') as f:
    f.write('sickrage|%s|%s|%s|%s|%s|%s' % (sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))
