"""
name: handler.py
description: Request handlers for file/part CRUD operations and download control
"""

from worker import file_threads, file_worker, ThreadData, file_threads_lock
from database import File, Part, database, database_lock, State
from loop import Code, loop
from threading import Thread, Event, Semaphore


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
    for attr in ("url", "path", "size", "state", "progress"):
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
        for attr in ("size", "state", "progress"):
            val = getattr(part, attr)
            if val is not None:
                setattr(base, attr, val)

        result = database.execute(
            "UPDATE parts SET size = ?, state = ?, progress = ? WHERE id = ? RETURNING *",
            (base.size, base.state, base.progress, base.id),
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


@loop.handler(Code.REQ_FILE_START)
def file_start(id: int):
    # Lock order: database_lock first, then file_threads_lock (consistent with file_stop)
    with database_lock:
        file = database.execute("SELECT * FROM files WHERE id = ? LIMIT 1", (id,)).fetchone()
        if file is None:
            return None
        file = File(*file)
    with file_threads_lock:
        if file.state == State.PENDING and file_threads.get(id) is not None:
            return file
    # Update file state to PENDING in database
    with database_lock:
        file = database.execute(
            "UPDATE files SET state = ? WHERE id = ? RETURNING *",
            (State.PENDING.value, id),
        ).fetchone()
    file = File(*file)
    with file_threads_lock:
        # Double-check to prevent concurrent file_start for the same file
        existing = file_threads.get(id)
        if existing is not None:
            return existing.value
        file_thread = Thread(target=file_worker, args=(file,), name=f"file-{id}", daemon=True)
        file_threads[id] = ThreadData(thread=file_thread, value=file, event_stop=Event(), semaphore=Semaphore(1), parts={})
    file_thread.start()
    return file


@loop.handler(Code.REQ_FILE_STOP)
def file_stop(id: int):
    with database_lock:
        file = database.execute("SELECT * FROM files WHERE id = ? LIMIT 1", (id,)).fetchone()
        if file is None:
            return None
        file = File(*file)
    with file_threads_lock:
        file_thread = file_threads.get(id)
        if file.state != State.PENDING and file_thread is None:
            return file
        if file_thread is not None:
            file_thread.event_stop.set()
        # Use pop with default to avoid KeyError if key doesn't exist
        file_threads.pop(file.id, None)
    with database_lock:
        file = database.execute("UPDATE files SET state = ? WHERE id = ? RETURNING *", (State.IDEL.value, id)).fetchone()
    file = File(*file) if file else None
    return file


def init():
    pass
