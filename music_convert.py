#!/usr/bin/env python3

# Converts music tracks to mp3 (if they are not already)

import sys
from pathlib import Path

try:
    basepath = Path(sys.argv[1])
except:
    print('Invalid directory to scan')
    sys.exit(1)
if not basepath.exists():
    print('Invalid directory to scan')
    sys.exit(1)
oldfile = ''
for file in basepath.rglob("*"):
    if file.is_file():
        if file.suffix == '.m4a':
            print(str(file))
