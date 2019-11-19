#!/usr/bin/env python

import sys

with open(f'/downloads/process/poll/{sys.argv[2]}.sonarr', 'w') as f:
    f.write('sonarr|%s|%s|%s' % (sys.argv[1], sys.argv[2], sys.argv[3]))
