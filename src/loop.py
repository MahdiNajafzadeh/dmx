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
