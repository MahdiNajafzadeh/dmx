"""
name: worker.py
description: Worker thread pool for parallel file download with progress tracking
"""

from dataclasses import dataclass
import httpx
from config import config
from loop import loop, Code
from log import log
from database import File, Part, State
from threading import Thread, Lock, Event, Semaphore
from typing import TypeVar

T = TypeVar("T", bound=object)


@dataclass
class PartThread:
    value: Part
    thread: Thread
    event_stop: Event


@dataclass
class FileThread:
    value: File
    thread: Thread
    event_stop: Event
    semaphore: Semaphore
    parts: dict[int, PartThread]


lock = Lock()
shared: dict[int, FileThread] = {}


def file_worker(file: File):
    try:
        with lock:
            if file.id not in shared:
                raise RuntimeError(f"access to file thread with id={file.id} in shared object")
        # calculate size of file
        res = httpx.head(file.url, follow_redirects=True)
        res.raise_for_status()
        size = int(res.headers.get("content-length", 0))
        # check empty file & skip
        if not size > 0:
            raise RuntimeError(f"for file.url with id={file.id} content-length is 0")
        # update size of file
        file.size = size
        loop.request(Code.REQ_FILE_UPDATE, file.id, file)
        # Create and pre-allocate the download file
        with open(file.path, "wb") as f:
            f.truncate(size)
        # calculate total section of file
        sections = int(config.get("PARALLEL_CONNECTION", 8))
        sections = sections if sections > 0 else 1
        log.info(f"set total section is {sections}")
        # update file thread in shared object
        with lock:
            if file.id not in shared:
                raise RuntimeError(f"access to file thread with id={file.id} in shared object")
            file_thread = shared[file.id]
            file_thread.semaphore = Semaphore(sections)
            event_stop = file_thread.event_stop
        parts: dict[int, PartThread] = {}
        # factory part threads
        for section in range(0, sections):
            part = loop.request(
                Code.REQ_PART_CREATE,
                Part(id=0, file_id=file.id, section=section, state=State.IDEL),
            )
            if part is None:
                raise RuntimeError(f"can not create a part record with section={section} for file with id={file.id}")
            thread = Thread(target=part_worker, args=(part,), name=f"part-{file.id}-{part.id}", daemon=True)
            part_thread = PartThread(
                value=part,
                thread=thread,
                event_stop=event_stop,
            )
            parts[part.id] = part_thread
            part_thread.thread.start()
            log.info(f"create a new part thread with section={part.id} for file with id={file.id}")
        """
        apppend part threads in part_threads shared object
        """
        file_thread.parts = parts
        """
        join & cleanup part threads
        """
        for idx in list(file_thread.parts.keys()):
            part_thread = file_thread.parts[idx]
            part_thread.thread.join()
            log.info(f"join part thread section={idx} for file with id={file.id}")
            log.info(f"cleanup part thread section={idx} for file with id={file.id}")
            file_thread.parts.pop(idx)
        with lock:
            if file.id in shared:
                log.info(f"cleanup file thread with id={file.id} from shared object")
                del shared[file.id]
        file.state = State.DONE
        loop.request(Code.REQ_FILE_UPDATE, file.id, file)
    except Exception as e:
        log.error(e)
        file.state = State.ERROR
        loop.request(Code.REQ_FILE_UPDATE, file.id, file)
        log.error(f"update file state={file.state} with id={file.id}")
        raise e
    finally:
        # rollback and cleanup (must hold lock to safely access shared dict)
        with lock:
            file_thread = shared.pop(file.id, None)
        if file_thread is not None:
            file_thread.event_stop.set()


file_threads = shared
file_threads_lock = lock
ThreadData = FileThread


def part_worker(part: Part):
    with lock:
        if part.file_id not in shared:
            raise RuntimeError(f"access to file thread with id={part.file_id} in shared object")
        file_thread = shared[part.file_id]
        file = file_thread.value
        if part.id not in file_thread.parts:
            raise RuntimeError(f"access to part thread with id={part.id} in file thread with id={part.file_id} in shared object")
        semaphore = file_thread.semaphore
    with semaphore:
        sections = int(config.get("PARALLEL_CONNECTION", 8))
        sections = sections if sections > 0 else 1
        part.size = file.size // sections
        loop.request(Code.REQ_PART_UPDATE, part.id, part)
        start_byte = part.section * part.size
        end_byte = start_byte + part.size - 1
        if part.section == sections - 1:
            end_byte = file.size - 1
        headers = {"Range": f"bytes={start_byte}-{end_byte}"}
        res = httpx.get(file.url, headers=headers)
        res.raise_for_status()
        part.state = State.PENDING
        loop.request(Code.REQ_PART_UPDATE, part.id, part)
        with open(file.path, "r+b") as f:
            f.seek(start_byte)
            download_length = 0
            for chunk in res.iter_bytes():
                if file_thread.event_stop.is_set():
                    part.state = State.IDEL
                    loop.request(Code.REQ_PART_UPDATE, part.id, part)
                    log.warning(f"part with id={part.id} for file with id={part.file_id} is stopped")
                    return
                if chunk:
                    f.write(chunk)
                    download_length += len(chunk)
                    progress = (download_length / (end_byte - start_byte + 1)) * 100
                    if int(progress) % 5 == 0:
                        part.progress = int(progress)
                        loop.request(Code.REQ_PART_UPDATE, part.id, part)
        part.state = State.DONE
        loop.request(Code.REQ_PART_UPDATE, part.id, part)
