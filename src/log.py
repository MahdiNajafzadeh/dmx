"""
name: log.py
description: logger, just init logger from loguru library
"""

import sys

from loguru import logger as log

log.remove()
log.add(sys.stdout, colorize=True, enqueue=True, format="{time} {level}: {message}")
