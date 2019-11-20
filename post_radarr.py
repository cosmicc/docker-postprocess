#!/usr/bin/env python

import sys

with open('/downloads/process/poll/%s.radarr' % (sys.argv[2],), 'w') as f:
    f.write('radarr|%s|%s|%s' % (sys.argv[1], sys.argv[2], sys.argv[3]))
