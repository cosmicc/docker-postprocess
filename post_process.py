#!/usr/bin/env python3

import os
import json
from loguru import logger as log

os.setgid(int(os.environ['PGID']))
os.setuid(int(os.environ['PUID']))

log.add(sink=str('/config/logs/poller.log'), level=3, buffering=1, enqueue=True, backtrace=False, diagnose=False, serialize=False, colorize=False, delay=False)


def main():
    log.info("Custom Post Process Script")

    files = json.loads(os.environ.get('MH_FILES'))

    for filename in files:
        log.info(filename)


if __name__ == "__main__":
    main()
