from dataclasses import dataclass
import httpx
from config import config
from loop import loop, Code
from log import log
from database import File, Part, database, database_lock, State
from threading import Thread, Lock, Event
from typing import TypeVar

T = TypeVar("T", bound=object)


@dataclass
class ThreadData[T]:
    thread: Thread
    value: T
    event_stop: Event


file_threads_lock = Lock()
file_threads: dict[int, ThreadData[File]] = {}
part_threads_lock = Lock()
part_threads: dict[int, dict[int, ThreadData[Part]]] = {}


def file_worker(file: File):
    try:
        res = httpx.head(file.url, follow_redirects=True)
        res.raise_for_status()
        size = int(res.headers.get("content-length", 0))
        file.size = size
        loop.request(Code.REQ_FILE_UPDATE, file.id, file)
        total_parts = int(
            min(
                config.get("PARALLEL_CONNECTION", 8),
                max(1, file.size // (1024 * 1024 * 10)),
            )
        )
        parts: dict[int, Part] = {}
        with part_threads_lock:
            for section in range(0, total_parts):
                part = loop.request(
                    Code.REQ_PART_CREATE,
                    file.id,
                    Part(id=0, file_id=file.id, section=section, state=State.IDEL),
                )
                if part is None:
                    raise RuntimeError(
                        f"can not create a part record with section={part.section} for file with id={file.id}"
                    )
                part = Part(*part)
                parts[part.id] = part
                log.info(
                    f"create a new part thread with section={part.id} for file with id={file.id}"
                )

    except Exception as e:
        file.state = State.ERROR
        loop.request(Code.REQ_FILE_UPDATE, file.id, file)
        raise e


def part_worker(part: File):
    pass
