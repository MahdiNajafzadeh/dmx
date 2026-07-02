from dataclasses import dataclass
from enum import IntEnum
from sqlite3 import connect
from threading import Lock

from config import config

database_lock = Lock()
database = connect(str(config.get("DATABASE_PATH")), check_same_thread=False)
database.executescript(
    """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    path TEXT NOT NULL,
    size INTEGER NOT NULL DEFAULT 0,
    state INTEGER NOT NULL DEFAULT 0,
    progress REAL NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    section INTEGER NOT NULL,
    size INTEGER NOT NULL DEFAULT 0,
    state INTEGER NOT NULL DEFAULT 0,
    progress REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (file_id) REFERENCES files(id)
);
"""
)


class State(IntEnum):
    IDEL = 0
    PENDING = 1
    ERROR = 2
    DONE = 3


@dataclass
class File:
    id: int
    url: str
    path: str
    size: int = 0
    state: State = State.IDEL
    progress: int = 0


@dataclass
class Part:
    id: int
    file_id: int
    section: int
    size: int = 0
    state: State = State.IDEL
    progress: int = 0
