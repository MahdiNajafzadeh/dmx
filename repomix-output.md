This file is a merged representation of a subset of the codebase, containing specifically included files, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: src/
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
src/
  api.py
  config.py
  database.py
  download.py
  handler.py
  log.py
  loop.py
  main.py
```

# Files

## File: src/config.py
```python
from os import environ
from log import log
from dotenv import load_dotenv
from types import MappingProxyType


log.info("load .env file")
load_dotenv()
log.success("load .env file")


log.info("init config")
config = MappingProxyType(
    {
        "PARALLEL_DOWNLOAD": int(str(environ.get("PARALLEL_DOWNLOAD", "2"))),
        "PARALLEL_CONNECTION": int(str(environ.get("PARALLEL_CONNECTION", "8"))),
        "DATABASE_PATH": str(environ.get("DATABASE_PATH", "main.db")),
        "HOST": str(environ.get("HOST", "0.0.0.0")),
        "PORT": int(str(environ.get("PORT", "3000"))),
    }
)
log.success("init config")
```

## File: src/handler.py
```python
from database import File, Part, database, database_lock
from loop import Code, loop


@loop.handler(Code.REQ_FILE_GET_ALL)
def get_all_file() -> list[File]:
    with database_lock:
        files = database.execute("SELECT * FROM files").fetchall()
        return [File(*file) for file in files]


@loop.handler(Code.REQ_FILE_GET)
def get_file(id: int) -> File | None:
    with database_lock:
        file = database.execute("SELECT * FROM files WHERE id = ?", (id,)).fetchone()
        return File(*file) if file else None


@loop.handler(Code.REQ_FILE_CREATE)
def create_file(file: File) -> File | None:
    with database_lock:
        result = database.execute(
            "INSERT INTO files (url, path) VALUES (?, ?) RETURNING *",
            (file.url, file.path),
        ).fetchone()
        return File(*result) if result else None


@loop.handler(Code.REQ_FILE_UPDATE)
def update_file(id: int, file: File) -> File | None:
    with database_lock:
        base = database.execute("SELECT * FROM files WHERE id = ?", (id,)).fetchone()
        if base is None:
            return None
        else:
            base = File(*base)
    for attr in ("ur", "path", "size", "state", "progress"):
        val = getattr(file, attr)
        if val is not None:
            setattr(base, attr, val)
    result = database.execute(
        "UPDATE files SET url = ?, path = ?, size = ?, state = ?, progress = ? WHERE id = ? RETURNING *",
        (base.url, base.path, base.size, base.state, base.progress, id),
    ).fetchone()
    return File(*result) if result else None


@loop.handler(Code.REQ_FILE_DELETE)
def delete_file(id: int) -> File | None:
    with database_lock:
        result = database.execute(
            "DELETE FROM files WHERE id = ? RETURNING *",
            (id,),
        ).fetchone()
        return File(*result) if result else None


@loop.handler(Code.REQ_PART_GET_ALL)
def get_all_part() -> list[Part]:
    with database_lock:
        parts = database.execute("SELECT * FROM parts").fetchall()
        return [Part(*row) for row in parts]


@loop.handler(Code.REQ_PART_GET)
def get_part(id: int) -> Part | None:
    with database_lock:
        result = database.execute(
            "SELECT * FROM parts WHERE id = ?",
            (id,),
        ).fetchone()
        return Part(*result) if result else None


@loop.handler(Code.REQ_PART_CREATE)
def create_part(part: Part) -> Part | None:
    with database_lock:
        result = database.execute(
            "INSERT INTO parts (file_id, section) VALUES (?, ?) RETURNING *",
            (part.file_id, part.section),
        ).fetchone()
        return Part(*result) if result else None


@loop.handler(Code.REQ_PART_UPDATE)
def update_part(id: int, part: Part) -> Part | None:
    with database_lock:
        base = database.execute("SELECT * FROM parts WHERE id = ?", (id,)).fetchone()
        if base is None:
            return None
        base = Part(*base)
        for attr in ("ur", "path", "size", "state", "progress"):
            val = getattr(part, attr)
            if val is not None:
                setattr(base, attr, val)

        result = database.execute(
            "UPDATE parts SET file_id = ?, section = ?, size = ?, state = ?, progress = ? WHERE id = ? RETURNING *",
            (base.file_id, base.section, base.size, base.state, base.progress, base.id),
        ).fetchone()
        return Part(*result) if result else None


@loop.handler(Code.REQ_PART_DELETE)
def delete_part(id: int) -> Part | None:
    with database_lock:
        result = database.execute(
            "DELETE FROM parts WHERE id = ? RETURNING *",
            (id,),
        ).fetchone()
        return Part(*result) if result else None


def init():
    pass
```

## File: src/api.py
```python
import uvicorn
from fastapi import FastAPI
from database import File
from loop import Code, loop
from config import config

app = FastAPI()


@app.get("/download")
async def get_all_download():
    return loop.request(Code.REQ_FILE_GET_ALL)


@app.get("/download/{id}")
async def get_download(id: int):
    return loop.request(Code.REQ_FILE_GET, id)


@app.post("/download")
async def create_download(download: File):
    return loop.request(Code.REQ_FILE_CREATE, download)


@app.patch("/download/{id}")
async def update_download(id: int, download: File):
    return loop.request(Code.REQ_FILE_UPDATE, id, download)


@app.delete("/download/{id}")
async def delete_download(id: int):
    return loop.request(Code.REQ_FILE_DELETE, id)


@app.post("/download/{id}/start")
async def start_download(id: int):
    return loop.request(Code.REQ_FILE_START, id)


@app.post("/download/{id}/stop")
async def stop_download(id: int):
    return loop.request(Code.REQ_FILE_STOP, id)


def init():
    uvicorn.run(app=app, host=str(config["HOST"]), port=int(config["PORT"]))
```

## File: src/database.py
```python
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
```

## File: src/download.py
```python
from database import File, Part, database, database_lock, State
from threading import Thread, Lock
from typing import TypeVar

T = TypeVar("T", bound=object)


class ThreadData[T]:
    thread: Thread
    value: T


file_threads_lock = Lock()
file_threads: dict[int, ThreadData[File]] = {}
part_threads_lock = Lock()
part_threads: dict[int, dict[int, ThreadData[Part]]] = {}


def file_worker():
    pass


def part_worker():
    pass
```

## File: src/log.py
```python
"""
name: log.py
description: logger, just init logger from loguru library
"""

import sys

from loguru import logger as log

log.remove()
log.add(sys.stdout, colorize=True, enqueue=True, format="{time} {level}: {message}")
```

## File: src/loop.py
```python
"""
name: loop.py
description: evet-loop is heart of system, all request must registry in this loop and use loop
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from queue import Queue
from threading import Condition
from typing import Any, Callable
from uuid import uuid4
from log import log


class Code(Enum):
    REQ_FILE_GET_ALL = auto()
    REQ_FILE_GET = auto()
    REQ_FILE_CREATE = auto()
    REQ_FILE_UPDATE = auto()
    REQ_FILE_DELETE = auto()
    REQ_FILE_START = auto()
    REQ_FILE_STOP = auto()
    REQ_PART_GET_ALL = auto()
    REQ_PART_GET = auto()
    REQ_PART_CREATE = auto()
    REQ_PART_UPDATE = auto()
    REQ_PART_DELETE = auto()
    REQ_PART_START = auto()
    REQ_PART_STOP = auto()


type Function = Callable[..., Any]


@dataclass
class Response:
    idx: str
    code: Code
    error: Exception | None = None
    result: Any = None


@dataclass
class Request:
    idx: str
    code: Code
    args: tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)


class Loop:
    def __init__(self) -> None:
        self._handlers: dict[Code, Function] = {}
        self._response: dict[str, Response] = {}
        self._running = True
        self._queue: Queue[Request] = Queue()
        self._notify = Condition()

    def handler(self, code: Code) -> Function:
        log.info(f"event-loop registry {code}")

        def wrapper(function: Function) -> Function:
            self._handlers[code] = function
            return function

        return wrapper

    def loop(self) -> None:
        while self._running:
            req = self._queue.get()
            handler = self._handlers.get(req.code)

            if handler is None:
                res = Response(
                    idx=req.idx,
                    code=req.code,
                    error=LookupError(f"handler not found: {req.code.name}"),
                )
            else:
                try:
                    res = Response(
                        idx=req.idx,
                        code=req.code,
                        result=handler(*req.args, **req.kwargs),
                    )
                except Exception as e:
                    res = Response(
                        idx=req.idx,
                        code=req.code,
                        error=e,
                    )

            with self._notify:
                self._response[req.idx] = res
                self._notify.notify_all()

    def request(self, code: Code, *args, **kwargs) -> Any:
        idx = uuid4().hex

        self._queue.put(
            Request(
                idx=idx,
                code=code,
                args=args,
                kwargs=kwargs,
            )
        )

        with self._notify:
            while self._running:
                res = self._response.pop(idx, None)
                if res is not None:
                    if res.error is not None:
                        raise res.error
                    return res.result
                self._notify.wait()

        raise RuntimeError("loop stopped")


loop = Loop()
```

## File: src/main.py
```python
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
    Thread(name="evet-loop", target=loop.loop),
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
```
