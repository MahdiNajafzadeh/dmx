"""
name: handler.py
description: Request handlers for file/part CRUD operations and download control
"""

from worker import lock, shared, FileThread, file_worker
from database import File, Part, database, database_lock, State
from loop import Code, loop
from threading import Thread, Event, Semaphore
from log import log


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
        cursor = database.cursor()
        try:
            cursor.execute("BEGIN")
            result = cursor.execute(
                "INSERT INTO files (url, path) VALUES (?, ?) RETURNING *",
                (file.url, file.path),
            ).fetchone()
            cursor.execute("COMMIT")
            return File(*result) if result else None
        except Exception as error:
            log.error(error)
            database.rollback()


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
    cursor = database.cursor()
    try:
        cursor.execute("BEGIN")
        result = cursor.execute("UPDATE files SET url = ?, path = ?, size = ?, state = ?, progress = ? WHERE id = ? RETURNING *", (base.url, base.path, base.size, base.state, base.progress, id)).fetchone()
        cursor.execute("COMMIT")
        return File(*result) if result else None
    except Exception as error:
        log.error(error)
        database.rollback()


@loop.handler(Code.REQ_FILE_DELETE)
def delete_file(id: int) -> File | None:
    with database_lock:
        cursor = database.cursor()
        try:
            cursor.execute("BEGIN")
            result = cursor.execute("DELETE FROM files WHERE id = ? RETURNING *", (id,)).fetchone()
            cursor.execute("COMMIT")
            return File(*result) if result else None
        except Exception as error:
            log.error(error)
            database.rollback()


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
        cursor = database.cursor()
        try:
            cursor.execute("BEGIN")
            result = cursor.execute("INSERT INTO parts (file_id, section) VALUES (?, ?) RETURNING *", (part.file_id, part.section)).fetchone()
            cursor.execute("COMMIT")
            return Part(*result) if result else None
        except Exception as error:
            log.error(error)
            database.rollback()


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

        cursor = database.cursor()
        try:
            cursor.execute("BEGIN")
            result = cursor.execute("UPDATE parts SET size = ?, state = ?, progress = ? WHERE id = ? RETURNING *", (base.size, base.state, base.progress, base.id)).fetchone()
            cursor.execute("COMMIT")
            return Part(*result) if result else None
        except Exception as error:
            log.error(error)
            database.rollback()


@loop.handler(Code.REQ_PART_DELETE)
def delete_part(id: int) -> Part | None:
    with database_lock:
        cursor = database.cursor()
        try:
            cursor.execute("BEGIN")
            result = cursor.execute("DELETE FROM parts WHERE id = ? RETURNING *", (id,)).fetchone()
            cursor.execute("COMMIT")
            return Part(*result) if result else None
        except Exception as error:
            log.error(error)
            database.rollback()


@loop.handler(Code.REQ_FILE_START)
def file_start(id: int):
    with database_lock:
        file = database.execute("SELECT * FROM files WHERE id = ? LIMIT 1", (id,)).fetchone()
        if file is None:
            return None
        file = File(*file)
    with lock:
        if file.state == State.PENDING and shared.get(id) is not None:
            return file
    with database_lock:
        c = database.cursor()
        try:
            c.execute("BEGIN")
            file = c.execute("UPDATE files SET state = ? WHERE id = ? RETURNING *", (State.PENDING.value, id)).fetchone()
            database.commit()
        except Exception as error:
            log.error(error)
            database.rollback()
            raise error

    file = File(*file)
    with lock:
        existing = shared.get(id)
        if existing is not None:
            return existing.value
        file_thread = Thread(target=file_worker, args=(file,), name=f"file-{id}", daemon=True)
        shared[id] = FileThread(thread=file_thread, value=file, event_stop=Event(), semaphore=Semaphore(1), parts={})
    file_thread.start()
    return file


@loop.handler(Code.REQ_FILE_STOP)
def file_stop(id: int):
    with database_lock:
        file = database.execute("SELECT * FROM files WHERE id = ? LIMIT 1", (id,)).fetchone()
        if file is None:
            return None
        file = File(*file)
    with lock:
        file_thread = shared.get(id)
        if file.state != State.PENDING and file_thread is None:
            return file
        if file_thread is not None:
            file_thread.event_stop.set()
        shared.pop(file.id, None)
    with database_lock:
        c = database.cursor()
        try:
            c.execute("BEGIN")
            file = c.execute("UPDATE files SET state = ? WHERE id = ? RETURNING *", (State.IDEL.value, id)).fetchone()
            c.execute("COMMIT")
        except Exception as error:
            log.error(error)
            database.rollback()
            raise error
    file = File(*file) if file else None
    return file


def init():
    pass
