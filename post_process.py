#!/usr/bin/env python3

import json
import os

from loguru import logger as log

os.setgid(int(os.environ['PGID']))
os.setuid(int(os.environ['PUID']))

log.add(sink=str('/config/logs/poller.log'), level=3, buffering=1, enqueue=True, backtrace=False, diagnose=False, serialize=False, colorize=False, delay=False)


def main():
    log.info("Custom post-process script starting...")

    try:
        files = json.loads(os.environ.get('MH_FILES'))
    except:
        log.exception('json load error')

    try:
        for filename in files:
            log.info(filename)
    except:
        log.exception('file loop error')


if __name__ == "__main__":
    main()
