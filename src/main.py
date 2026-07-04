"""
name: main.py
description: bootstrap all components
"""

from threading import Thread
from loop import loop
from api import init as api_init
from handler import init as handler_init
from log import log


threads: list[Thread] = [
    Thread(name="event-loop", target=loop.loop),
    Thread(name="api", target=api_init),
    Thread(name="download", target=handler_init),
]


def main():
    for thread in threads:
        log.info(f"start new thread {thread.name}")
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
