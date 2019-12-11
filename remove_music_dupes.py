#!/usr/bin/env python3

# Removes duplicate tracks from albums

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
        dupefile = Path(f'{file.parent}/{file.stem}.1{file.suffix}')
        dupefile2 = Path(f'{file.parent}/{file.stem}.2{file.suffix}')
        dupefile3 = Path(f'{file.parent}/{file.stem}.3{file.suffix}')
        if str(file.name) == oldfile:
            print(f'Duplicate Found: {str(file)}')
        oldfile = str(file.name)
        # print(f'{str(file).strip()} -> {oldfile.strip()}')
        if dupefile3.exists():
            print(str(dupefile3))
        if dupefile.exists():
            if dupefile.stat().st_size <= file.stat().st_size:
                if dupefile2.exists():
                    if dupefile2.stat().st_size <= file.stat().st_size:
                        dupfile2.unlink()
                        print(f'Deleted: {str(dupefile)}')
                    else:
                        file.unlink()
                        dupfile2.rename(file)
                        print(f'Replaced: {str(file)} <- {str(dupefile)}')
                else:
                    dupefile.unlink()
                    print(f'Deleted: {str(dupefile)}')
            else:
                file.unlink()
                dupefile.rename(file)
                print(f'Replaced: {str(file)} <- {str(dupefile)}')
        elif dupefile2.exists():
            if dupefile2.stat().st_size <= file.stat().st_size:
                dupefile2.unlink()
                print(f'Deleted: {str(dupefile2)}')
            else:
                file.unlink()
                dupefile2.rename(file)
                print(f'Replaced: {str(file)} <- {str(dupefile2)}')


    
