### Basic Multiprocessing with Loguru on Windows

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

This example demonstrates a basic setup for using Loguru with `multiprocessing.Process` on Windows. It removes the default handler and adds a file handler with `enqueue=True` to ensure picklability.

```python
import multiprocessing
from loguru import logger

def my_process(logger_):
    logger_.info("Executing function in child process")
    logger_.complete()

if __name__ == "__main__":
    logger.remove()  # Default "sys.stderr" sink is not picklable
    logger.add("file.log", enqueue=True)

    process = multiprocessing.Process(target=my_process, args=(logger, ))
    process.start()
    process.join()

    logger.info("Done")
```

--------------------------------

### Install Development Dependencies

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Install Loguru in development mode.

```bash
$ pip install -e ".[dev]"
```

--------------------------------

### Install Loguru

Source: https://github.com/delgan/loguru/blob/master/README.md

Use pip to install the Loguru library. This command should be run in your terminal or command prompt.

```bash
pip install loguru
```

--------------------------------

### Install Pre-commit Hooks

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Install hooks to automatically check commits.

```bash
$ pre-commit install --install-hooks
```

--------------------------------

### Deprecated start() function

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

The `start()` function is deprecated since version 0.2.2 and will be removed in Loguru 1.0.0. It is replaced by the `add()` function.

```APIDOC
## Deprecated start() function

### Description
This function is deprecated and will be removed in a future version. Use `add()` instead.

### Method
N/A (This is a function call, not an API endpoint)

### Endpoint
N/A

### Parameters
N/A

### Request Example
```python
# Deprecated usage:
# logger.start(...)

# Recommended usage:
logger.add(...)
```

### Response
N/A
```

--------------------------------

### Install loguru-mypy Plugin

Source: https://github.com/delgan/loguru/blob/master/docs/api/type_hints.md

Installs the `loguru-mypy` plugin using pip, which provides additional type checking capabilities for Loguru.

```bash
pip install loguru-mypy
```

--------------------------------

### Log output with unknown source

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

Example of log output when the logger cannot retrieve the caller's context.

```none
2024-12-01 16:23:21.769 | INFO     | None:<unknown>:0 - Message from unknown source.
```

--------------------------------

### Mypy Output for Type Hint Example

Source: https://github.com/delgan/loguru/blob/master/docs/api/type_hints.md

Shows the output from the `mypy` type checker when analyzing the provided Python code with type hints.

```text
$ mypy test.py
test.py:8: error: TypedDict "Record" has no key 'invalid'
Found 1 error in 1 file (checked 1 source file)
```

--------------------------------

### Lifecycle Management

Source: https://github.com/delgan/loguru/blob/master/docs/api/type_hints_source.md

Methods to control the start and stop state of the logger.

```APIDOC
## start() / stop()

### Description
Manages the lifecycle of the logger instance.

### Response
#### Success Response (200)
- **start()** returns (int) - The identifier of the started logger instance.
```

--------------------------------

### Configure Loguru for Scripts

Source: https://github.com/delgan/loguru/blob/master/docs/overview.md

Set up Loguru handlers and extra context for script usage using `logger.configure()`. This example adds a stdout handler with a simple format and a file handler that serializes logs.

```python
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": "file.log", "serialize": True},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)
```

--------------------------------

### Test log capture with custom context manager

Source: https://github.com/delgan/loguru/blob/master/docs/resources/migration.md

Example usage of the `capture_logs` context manager to test functions that produce log messages.

```python
def do_something(val):
    if val < 0:
        logger.error("Invalid value")
        return 0
    return val * 2


class TestDoSomething(unittest.TestCase):
    def test_do_something_good(self):
        with capture_logs() as output:
            do_something(1)
        self.assertEqual(output, [])

    def test_do_something_bad(self):
        with capture_logs() as output:
            do_something(-1)
        self.assertEqual(len(output), 1)
        message = output[0]
        self.assertIn("Invalid value", message)
        self.assertEqual(message.record["level"].name, "ERROR")
```

--------------------------------

### Example test using pytest caplog

Source: https://github.com/delgan/loguru/blob/master/docs/resources/migration.md

Demonstrates a basic test case that uses pytest's caplog fixture to capture and assert logging messages.

```python
from loguru import logger

def some_func(a, b):
    if a < 0:
        logger.warning("Oh no!")
    return a + b

def test_some_func(caplog):
    assert some_func(-1, 3) == 2
    assert "Oh no!" in caplog.text
```

--------------------------------

### Using Loguru with multiprocessing.Pool and Initializers

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

This example shows how to use Loguru with `multiprocessing.Pool` by leveraging the `initializer` and `initargs` parameters. It demonstrates two methods: using a worker class and using a global function to set the logger for worker processes.

```python
# main.py
from multiprocessing import Pool
from loguru import logger
import workers_a
import workers_b

if __name__ == "__main__":
    logger.remove()
    logger.add("file.log", enqueue=True)

    worker = workers_a.Worker()
    with Pool(4, initializer=worker.set_logger, initargs=(logger, )) as pool:
        results = pool.map(worker.work, [1, 10, 100])

    with Pool(4, initializer=workers_b.set_logger, initargs=(logger, )) as pool:
        results = pool.map(workers_b.work, [1, 10, 100])

    logger.info("Done")
```

--------------------------------

### Specifying Multiprocessing Context with Loguru

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

This example demonstrates how to explicitly specify the multiprocessing context when adding a Loguru handler with `enqueue=True`. This is crucial for preventing issues when subprocesses are created with a different context than the parent process.

```python
import multiprocessing
from loguru import logger
import workers_a

if __name__ == "__main__":
    context = multiprocessing.get_context("spawn")

    logger.remove()
    logger.add("file.log", enqueue=True, context=context)

    worker = workers_a.Worker()
    with context.Pool(4, initializer=worker.set_logger, initargs=(logger, )) as pool:
        results = pool.map(worker.work, [1, 10, 100])
```

--------------------------------

### Log exception with traceback

Source: https://github.com/delgan/loguru/blob/master/README.md

Logs an exception with a full traceback when a ZeroDivisionError occurs. This example demonstrates how Loguru captures and displays detailed error information.

```python
def func(a, b):
    return a / b

def nested(c):
    try:
        func(5, c)
    except ZeroDivisionError:
        logger.exception("What?!")

nested(0)
```

--------------------------------

### Check Loguru Version

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Use this command to identify the installed version of Loguru for bug reports.

```python
print(loguru.__version__)
```

--------------------------------

### Configure Loguru for Scripts and Libraries

Source: https://github.com/delgan/loguru/blob/master/README.md

Configure Loguru at the start of your script. For libraries, use `disable()` to prevent log calls from executing and `enable()` to allow them.

```python
# For scripts
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": "file.log", "serialize": True},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)

# For libraries, should be your library's `__name__`
logger.disable("my_library")
logger.info("No matter added sinks, this message is not displayed")

# In your application, enable the logger in the library
logger.enable("my_library")
logger.info("This message however is propagated to the sinks")
```

--------------------------------

### Correct Message Formatting with Placeholder

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example shows the recommended way to log messages containing data structures by using Loguru's built-in formatting with placeholders, avoiding f-string interpolation issues.

```python
logger.info("Processing '{data}'", data=data)
```

--------------------------------

### Configure Log Colors with Special Tags

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

Ensure color tags are included in the format string for handlers to enable colored logs. This example shows how to add a handler with a custom format including color tags.

```python3
logger.add(sys.stderr, format="<green>{time}</green> | <level>{message}</level>")
```

--------------------------------

### Loguru Formatting Error: KeyError

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example demonstrates a `KeyError` that occurs when the message string contains placeholders (e.g., `{key1, key2}`) that do not match the provided keyword arguments.

```python
# KeyError: 'key1, key2'
logger.warning("Config file missing keys: {key1, key2}", filename="app.cfg")
```

--------------------------------

### Customize Log Format with Basic String

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

Define a custom log message format using the `format` argument in the `add()` method. This example uses a simple time, level, and message structure.

```python
logger.add(sys.stderr, format="{time} - {level} - {message}")
```

--------------------------------

### Attaching Sinks to Named Loggers

Source: https://github.com/delgan/loguru/blob/master/docs/resources/migration.md

Use `bind()` to create named loggers and attach specific sinks to them. This example ensures messages from logger 'a' go to 'a.log' and messages from logger 'b' go to 'b.log'.

```python
# Only write messages from "a" logger
logger.add("a.log", filter=lambda record: record["extra"].get("name") == "a")
# Only write messages from "b" logger
logger.add("b.log", filter=lambda record: record["extra"].get("name") == "b")

logger_a = logger.bind(name="a")
logger_b = logger.bind(name="b")

logger_a.info("Message A")
logger_b.info("Message B")
```

--------------------------------

### Configure Loguru Logger

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

The `logger.configure()` method allows comprehensive setup of the logger. It can set up handlers, define custom levels, bind global `extra` data, specify a `patcher` function for record modification, and control logger activation states.

```python
>>> logger.configure(
...     handlers=[
...         dict(sink=sys.stderr, format="[{time}] {message}"),
...         dict(sink="file.log", enqueue=True, serialize=True),
...     ],
...     levels=[dict(name="NEW", no=13, icon="¤", color="")],
...     extra={"common_to_all": "default"},
...     patcher=lambda record: record["extra"].update(some_value=42),
...     activation=[("my_module.secret", False), ("another_library.module", True)],
... )
[1, 2]
```

```python
>>> # Set a default "extra" dict to logger across all modules, without "bind()"
>>> extra = {"context": "foo"}
>>> logger.configure(extra=extra)
>>> logger.add(sys.stderr, format="{extra[context]} - {message}")
>>> logger.info("Context without bind")
>>> # => "foo - Context without bind"
>>> logger.bind(context="bar").info("Suppress global context")
>>> # => "bar - Suppress global context"
```

--------------------------------

### Initialize global configuration

Source: https://context7.com/delgan/loguru/llms.txt

Use configure() to set up handlers, levels, and defaults globally.

```python
import sys
from loguru import logger
```

--------------------------------

### Full Configuration in One Call

Source: https://context7.com/delgan/loguru/llms.txt

Configure all Loguru handlers, levels, patchers, and activation rules with a single dictionary passed to the `configure` method. This is useful for setting up complex logging scenarios at application startup.

```python
import sys
from loguru import logger

config = {
    "handlers": [
        {
            "sink": sys.stderr,
            "format": "{time:HH:mm:ss} | {level: <8} | {message}",
            "level": "DEBUG",
            "colorize": True
        },
        {
            "sink": "logs/app.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}",
            "level": "INFO",
            "rotation": "1 day",
            "retention": "7 days",
            "compression": "zip",
            "enqueue": True
        },
        {
            "sink": "logs/errors.log",
            "level": "ERROR",
            "serialize": True
        }
    ],
    "levels": [
        {"name": "AUDIT", "no": 35, "icon": "📋", "color": "<blue>"}
    ],
    "extra": {"app_name": "MyApp", "version": "1.0.0"},
    "patcher": lambda record: record["extra"].update(hostname="server1"),
    "activation": [
        ("", True),                  # Enable all by default
        ("noisy_module", False),     # Disable specific module
    ]
}

handler_ids = logger.configure(**config)
print(f"Added handlers: {handler_ids}")

# Extra values are available in all log messages
logger.info("Application started")
# Output includes: {'app_name': 'MyApp', 'version': '1.0.0', 'hostname': 'server1'}
```

--------------------------------

### Various usages of opt() method

Source: https://github.com/delgan/loguru/blob/master/README.md

Demonstrates different functionalities of the opt() method, including exception logging, colorization, record display, raw output, stack context, and controlling extra attribute capture.

```python
logger.opt(exception=True).info("Error stacktrace added to the log message (tuple accepted too)")
logger.opt(colors=True).info("Per message <blue>colors</blue>")
logger.opt(record=True).info("Display values from the record (eg. {record[thread]})")
logger.opt(raw=True).info("Bypass sink formatting\n")
logger.opt(depth=1).info("Use parent stack context (useful within wrapped functions)")
logger.opt(capture=False).info("Keyword arguments not added to {dest} dict", dest="extra")
```

--------------------------------

### Initialize and use the Loguru logger

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

Import the global logger instance to begin logging messages immediately.

```python3
from loguru import logger

logger.info("Hello, World!")
```

--------------------------------

### Demonstrate UnicodeEncodeError

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Example of a scenario where printing unsupported characters triggers a UnicodeEncodeError in certain environments.

```python
print("天")
# UnicodeEncodeError: 'charmap' codec can't encode character '\u5929' in position 0: character maps to <undefined>
```

--------------------------------

### Replace Standard Logging Handlers with Loguru

Source: https://github.com/delgan/loguru/blob/master/docs/resources/migration.md

Demonstrates the transition from manual handler configuration to Loguru's unified add() method.

```python3
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("spam.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
```

```python3
fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)
```

--------------------------------

### Run Unit Tests

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Execute the test suite using tox.

```bash
$ tox -e tests
```

--------------------------------

### IndentationError Example in Python

Source: https://github.com/delgan/loguru/blob/master/tests/exceptions/output/diagnose/indentation_error.txt

This code snippet, when executed, will raise an IndentationError due to faulty indentation. The traceback clearly indicates the problematic line.

```python
exec(
"if True:
    a = 5
        print(\"foobar\")  #intentional faulty indentation here.
    b = 7
")
```

--------------------------------

### Activate Virtual Environment

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Commands to create and activate a virtual environment for development.

```bash
$ python -m venv env
$ source env/bin/activate
```

--------------------------------

### Print Logger to Check Handlers

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

Print the logger object to get an overview of configured handlers. This is useful for verifying that at least one sink has been added.

```python3
print(logger)
# Output: <loguru.logger handlers=[(id=0, level=10, sink=<stderr>)]>
```

--------------------------------

### Basic Type Hint Usage with Loguru

Source: https://github.com/delgan/loguru/blob/master/docs/api/type_hints.md

Demonstrates how to use Loguru's type hints for sinks and filters. Requires `from __future__ import annotations` for Python 3.7+.

```python
from __future__ import annotations

import loguru
from loguru import logger

def good_sink(message: loguru.Message):
    print("My name is", message.record["name"])

def bad_filter(record: loguru.Record):
    return record["invalid"]

logger.add(good_sink, filter=bad_filter)
```

--------------------------------

### Get custom level info with `level()` in Loguru

Source: https://github.com/delgan/loguru/blob/master/docs/resources/migration.md

Retrieve custom level details (name, number, color, icon) using `logger.level('LEVEL_NAME')`.

```python
logger.getLevelName(33)  # => "CUSTOM"
logger.level("CUSTOM")   # => (name='CUSTOM', no=33, color="<red>", icon="🚨")
```

--------------------------------

### Create Development Branch

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Commands to create and switch to a new branch for development.

```bash
$ git checkout master
$ git branch fix_bug
$ git checkout fix_bug
```

--------------------------------

### Custom Time Format

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

Set a custom time format directly in the handler's format specifier. This example uses HH:mm:ss for the time.

```python
format="{time:HH:mm:ss} {message}"
```

--------------------------------

### Loguru Formatting Error: ValueError

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example shows a `ValueError` caused by an unescaped single curly brace `{` in the message string, which Loguru interprets as an incomplete placeholder.

```python
# ValueError: Single '{' encountered in format string
logger.info("This is a curly bracket: {", foo="bar")
```

--------------------------------

### Configure file logging with rotation and retention

Source: https://context7.com/delgan/loguru/llms.txt

Set up file sinks with automated rotation, retention policies, and compression options for log management.

```python
from loguru import logger

# Basic file logging with timestamp in filename
logger.add("logs/app_{time}.log")

# Rotation by file size
logger.add("logs/size_rotate.log", rotation="500 MB")

# Rotation by time
logger.add("logs/daily.log", rotation="00:00")  # Rotate at midnight
logger.add("logs/hourly.log", rotation="1 hour")
logger.add("logs/weekly.log", rotation="1 week")

# Multiple rotation conditions (rotates when any condition is met)
logger.add("logs/multi.log", rotation=["100 MB", "00:00"])

# Retention policy - keep only recent logs
logger.add("logs/retained.log", rotation="1 day", retention="10 days")
logger.add("logs/retained_count.log", rotation="1 MB", retention=5)  # Keep 5 files

# Compression of rotated files
logger.add("logs/compressed.log", rotation="50 MB", compression="zip")
logger.add("logs/compressed_gz.log", rotation="50 MB", compression="gz")

# Complete configuration example
logger.add(
    "logs/production.log",
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}",
    encoding="utf-8",
    enqueue=True  # Thread-safe, non-blocking
)

logger.info("Logging to file with rotation enabled")
```

--------------------------------

### reinstall()

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

Reinstalls the core of the logger, useful for multiprocessing scenarios when using spawn.

```APIDOC
## reinstall()

### Description
Reinstall the core of logger. When using multiprocessing, you can pass logger as a parameter to the target of multiprocessing.Process, and run this method once.

### Method
Method call

### Parameters
None
```

--------------------------------

### Loguru Formatting Error: AttributeError

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example illustrates an `AttributeError` that can occur if a dictionary is passed as a positional argument to a logging function, and the message string attempts to format it incorrectly.

```python
# AttributeError: 'dict' object has no attribute 'format'
logger.debug({"key": "value"}, identifier=42)
```

--------------------------------

### Configurable File Logging Options

Source: https://github.com/delgan/loguru/blob/master/README.md

Configure file logging with rotation based on size or time, retention policies to clean up old logs, and compression to save space.

```python
logger.add("file_1.log", rotation="500 MB")
```

```python
logger.add("file_2.log", rotation="12:00")
```

```python
logger.add("file_3.log", rotation="1 week")
```

```python
logger.add("file_X.log", retention="10 days")
```

```python
logger.add("file_Y.log", compression="zip")
```

--------------------------------

### Loguru Formatting Error: IndexError

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example demonstrates an `IndexError` that arises when the message string expects positional arguments (e.g., `{}`) but receives keyword arguments instead, or if the indices are mismatched.

```python
# IndexError: Replacement index 0 out of range for positional args tuple
logger.error("Use 'set()' not '{}' for empty set", strictness=9)
```

--------------------------------

### Define Loguru Type Hints and Configurations

Source: https://github.com/delgan/loguru/blob/master/docs/api/type_hints_source.md

Contains the core type definitions, protocols for handlers, and TypedDict configurations for basic, file, and async log handlers.

```python
import sys
from asyncio import AbstractEventLoop
from datetime import datetime, time, timedelta
from logging import Handler
from multiprocessing.context import BaseContext
from types import TracebackType
from typing import (
    Any,
    BinaryIO,
    Callable,
    Dict,
    Generator,
    Generic,
    List,
    NamedTuple,
    NewType,
    Optional,
    Pattern,
    Sequence,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

if sys.version_info >= (3, 6):
    from typing import Awaitable
else:
    from typing_extensions import Awaitable

if sys.version_info >= (3, 6):
    from os import PathLike
    from typing import ContextManager

    PathLikeStr = PathLike[str]
else:
    from pathlib import PurePath as PathLikeStr

    from typing_extensions import ContextManager

if sys.version_info >= (3, 8):
    from typing import Protocol, TypedDict
else:
    from typing_extensions import Protocol, TypedDict

_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Any])
ExcInfo = Tuple[Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]]

class _GeneratorContextManager(ContextManager[_T], Generic[_T]):
    def __call__(self, func: _F) -> _F: ...
    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]: ...

Catcher = NewType("Catcher", _GeneratorContextManager[None])
Contextualizer = NewType("Contextualizer", _GeneratorContextManager[None])
AwaitableCompleter = Awaitable[None]

class Level(NamedTuple):
    name: str
    no: int
    color: str
    icon: str

class _RecordAttribute:
    def __format__(self, spec: str) -> str: ...

class RecordFile(_RecordAttribute):
    name: str
    path: str

class RecordLevel(_RecordAttribute):
    name: str
    no: int
    icon: str

class RecordThread(_RecordAttribute):
    id: int
    name: str

class RecordProcess(_RecordAttribute):
    id: int
    name: str

class RecordException(NamedTuple):
    type: Optional[Type[BaseException]]
    value: Optional[BaseException]
    traceback: Optional[TracebackType]

class Record(TypedDict):
    elapsed: timedelta
    exception: Optional[RecordException]
    extra: Dict[Any, Any]
    file: RecordFile
    function: str
    level: RecordLevel
    line: int
    message: str
    module: str
    name: Optional[str]
    process: RecordProcess
    thread: RecordThread
    time: datetime

class Message(str):
    record: Record

class Writable(Protocol):
    def write(self, message: Message) -> Any: ...

FilterDict = Dict[Optional[str], Union[str, int, bool]]
FilterFunction = Callable[[Record], bool]
FormatFunction = Callable[[Record], str]
PatcherFunction = Callable[[Record], None]
RotationFunction = Callable[[Message, TextIO], bool]
RetentionFunction = Callable[[List[str]], None]
CompressionFunction = Callable[[str], None]

StandardOpener = Callable[[str, int], int]

class BasicHandlerConfig(TypedDict, total=False):
    sink: Union[TextIO, Writable, Callable[[Message], None], Handler]
    level: Union[str, int]
    format: Union[str, FormatFunction]
    filter: Optional[Union[str, FilterFunction, FilterDict]]
    colorize: Optional[bool]
    serialize: bool
    backtrace: bool
    diagnose: bool
    enqueue: bool
    catch: bool

class FileHandlerConfig(TypedDict, total=False):
    sink: Union[str, PathLikeStr]
    level: Union[str, int]
    format: Union[str, FormatFunction]
    filter: Optional[Union[str, FilterFunction, FilterDict]]
    colorize: Optional[bool]
    serialize: bool
    backtrace: bool
    diagnose: bool
    enqueue: bool
    catch: bool
    rotation: Optional[
        Union[
            str,
            int,
            time,
            timedelta,
            RotationFunction,
            list[Union[str, int, time, timedelta, RotationFunction]],
        ]
    ]
    retention: Optional[Union[str, int, timedelta, RetentionFunction]]
    compression: Optional[Union[str, CompressionFunction]]
    delay: bool
    watch: bool
    mode: str
    buffering: int
    encoding: str
    errors: Optional[str]
    newline: Optional[str]
    closefd: bool
    opener: Optional[StandardOpener]

class AsyncHandlerConfig(TypedDict, total=False):
    sink: Callable[[Message], Awaitable[None]]
    level: Union[str, int]
    format: Union[str, FormatFunction]
    filter: Optional[Union[str, FilterFunction, FilterDict]]
    colorize: Optional[bool]
    serialize: bool
    backtrace: bool
    diagnose: bool
    enqueue: bool
    catch: bool
    context: Optional[Union[str, BaseContext]]
    loop: Optional[AbstractEventLoop]

HandlerConfig = Union[BasicHandlerConfig, FileHandlerConfig, AsyncHandlerConfig]

class LevelConfig(TypedDict, total=False):
    name: str
    no: int
    color: str
    icon: str

ActivationConfig = Tuple[Optional[str], bool]

class Logger:
    @overload
    def add(
        self,
```

--------------------------------

### Loguru Message Formatting with Arguments

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

Loguru integrates positional or keyword arguments into the message using a mechanism similar to Python's `str.format()`. This example shows a correct usage.

```python
logger.info("My name is {name}", name="John")
# Output: [INFO] My name is John
```

--------------------------------

### Configure File Rotation, Retention, and Compression

Source: https://github.com/delgan/loguru/blob/master/docs/overview.md

Advanced file logging configuration for rotation, retention, and compression.

```python
logger.add("file_1.log", rotation="500 MB")    # Automatically rotate too big file
logger.add("file_2.log", rotation="12:00")     # New file is created each day at noon
logger.add("file_3.log", rotation="1 week")    # Once the file is too old, it's rotated

logger.add("file_X.log", retention="10 days")  # Cleanup after some time

logger.add("file_Y.log", compression="zip")    # Save some loved space
```

--------------------------------

### Adding a Filtered Sink with Loguru

Source: https://github.com/delgan/loguru/blob/master/docs/resources/migration.md

Configure a sink to log only specific messages by providing a filter function. This example logs messages that have 'specific' in their `record["extra"]` dictionary.

```python
def specific_only(record):
    return "specific" in record["extra"]

logger.add("specific.log", filter=specific_only)

specific_logger = logger.bind(specific=True)

logger.info("General message")          # This is filtered-out by the specific sink
specific_logger.info("Module message")  # This is accepted by the specific sink (and others)
```

--------------------------------

### Loguru Formatting Error with f-string and Dictionary

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example shows how using an f-string can inadvertently embed curly braces from a dictionary representation into the log message, leading to a `KeyError` when Loguru tries to format it.

```python
data = {"foo": 42}

# Will raise "KeyError" because it's equivalent to:
#   logger.info("Processing '{'foo': 42}'", data=data)
logger.info(f"Processing '{data}'", data=data)
```

--------------------------------

### Clone Repository

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Commands to clone the Loguru repository locally.

```bash
$ git clone git@github.com:your_name_here/loguru.git
$ cd loguru
```

--------------------------------

### Add log file with backtrace and diagnose

Source: https://github.com/delgan/loguru/blob/master/README.md

Configure a log file sink with backtrace and diagnose enabled. Caution: diagnose=True may leak sensitive data in production.

```python
logger.add("out.log", backtrace=True, diagnose=True)
```

--------------------------------

### Various Usages of `opt()` Method

Source: https://github.com/delgan/loguru/blob/master/docs/overview.md

The `opt()` method provides several utilities for customizing log message handling, including enabling exception tracing, applying per-message colors, displaying record data, bypassing sink formatting, using parent stack context, and controlling keyword argument capture.

```python
# By the way, "opt()" serves many usages
logger.opt(exception=True).info("Error stacktrace added to the log message (tuple accepted too)")
logger.opt(colors=True).info("Per message <blue>colors</blue>")
logger.opt(record=True).info("Display values from the record (eg. {record[thread]})")
logger.opt(raw=True).info("Bypass sink formatting\n")
logger.opt(depth=1).info("Use parent stack context (useful within wrapped functions)")
logger.opt(capture=False).info("Keyword arguments not added to {dest} dict", dest="extra")
```

--------------------------------

### Demonstrate Exception Catching with Decorator

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

This example shows how the @logger.catch decorator handles exceptions. When a function decorated with @logger.catch raises an exception, it is logged. The 'reraise' parameter defaults to False, meaning the exception is caught and logged but not propagated further by default.

```python
>>> @logger.catch
... def f(x):
...     100 / x
...
>>> def g():
...     f(10)
...     f(0)
...
>>> g()
ERROR - An error has been caught in function 'g', process 'Main' (367), thread 'ch1' (1398):
Traceback (most recent call last):
  File "program.py", line 12, in <module>
    g()
    └ <function g at 0x7f225fe2bc80>
> File "program.py", line 10, in g
    f(0)
    └ <function f at 0x7f225fe2b9d8>
  File "program.py", line 6, in f
    100 / x
          └ 0
ZeroDivisionError: division by zero

```

--------------------------------

### Configure file permissions for log files

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Uses the opener argument in logger.add to set specific file permissions via os.open.

```python
def opener(file, flags):
    return os.open(file, flags, 0o600)  # read/write by owner only

logger.add("foo.log", rotation="100 kB", opener=opener)
```

--------------------------------

### Logger.reinstall() Method

Source: https://github.com/delgan/loguru/blob/master/docs/api/type_hints_source.md

Reinstalls the logger, resetting its configuration to the default state.

```APIDOC
## Logger.reinstall()

### Description
Reinstalls the logger, resetting its configuration to the default state.

### Method
`reinstall`

### Parameters
None

### Request Example
None

### Response
#### Success Response (200)
Returns `None`.

#### Response Example
None
```

--------------------------------

### Preventing Deadlock with a Filtered Sink

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example demonstrates how to prevent 'RuntimeError: deadlock avoided' by using a filter to stop recursive logging calls. The `avoid_recursion` filter ensures that the `my_sink` function, which itself calls the logger, does not trigger another logging event.

```python
import sys
from loguru import logger


def my_sink(message):
    logger.debug("Within my sink")
    print(message, end="")


def avoid_recursion(record):
    return record["function"] != "my_sink"


if __name__ == "__main__":
    logger.remove()
    logger.add("file.log")
    logger.add(my_sink, filter=avoid_recursion)

    logger.info("First message")
    logger.debug("Another message")
```

--------------------------------

### Add a Handler with Formatting and Filtering

Source: https://github.com/delgan/loguru/blob/master/README.md

Use the `add()` function to register sinks with custom formatting, filtering, and log levels. This is the primary way to configure Loguru's output.

```python
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
```

--------------------------------

### Illustrate I/O Error on Closed File with StringIO

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example demonstrates how a logger can inadvertently use a closed stream object, leading to an 'I/O operation on closed file' error. It highlights the issue when `sys.stdout` is redirected and then closed by an external context manager.

```python
from contextlib import contextmanager
import sys
import io
from loguru import logger


@contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target
        new_target.close()


if __name__ == "__main__":
    logger.remove()
    f = io.StringIO()

    with redirect_stdout(f):
        logger.add(sys.stdout)  # Logger is inadvertently configured with wrapped stream.
        logger.info("Hello")
        output = f.getvalue()

    print(f"Captured output: {output}")

    # ValueError: I/O operation on closed file.
    logger.info("World")
```

--------------------------------

### Creating independent loggers with bind and filter

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Route logs to specific files by binding extra context and filtering handlers based on that context.

```python
from loguru import logger

def task_A():
    logger_a = logger.bind(task="A")
    logger_a.info("Starting task A")
    do_something()
    logger_a.success("End of task A")

def task_B():
    logger_b = logger.bind(task="B")
    logger_b.info("Starting task B")
    do_something_else()
    logger_b.success("End of task B")

logger.add("file_A.log", filter=lambda record: record["extra"]["task"] == "A")
logger.add("file_B.log", filter=lambda record: record["extra"]["task"] == "B")

task_A()
task_B()
```

--------------------------------

### Send raw log messages

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

Use opt(raw=True) to bypass sink formatting and send the log message directly as is. This is useful when sinks are expected to handle all formatting.

```python
>>> logger.opt(raw=True).debug("No formatting\n")
...
```

--------------------------------

### Handle Exceptions with onerror and sys.exit

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

This example demonstrates using the 'onerror' parameter with @logger.catch to execute a function when an error occurs. Here, sys.exit(1) is called to ensure a non-zero exit code, preventing the program from appearing successful when an error is caught and 'reraise' is False.

```python
# Use 'onerror' to prevent the program exit code to be 0 (if 'reraise=False') while
>>> # also avoiding the stacktrace to be duplicated on stderr (if 'reraise=True').
>>> @logger.catch(onerror=lambda _: sys.exit(1))
... def main():
...     1 / 0

```

--------------------------------

### Create dynamic log formatting and coloring

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Use formatting functions to apply dynamic colors or styles based on record attributes or message content.

```python
from collections import defaultdict
from random import choice

colors = ["blue", "cyan", "green", "magenta", "red", "yellow"]
color_per_module = defaultdict(lambda: choice(colors))

def formatter(record):
    color_tag = color_per_module[record["name"]]
    return "<" + color_tag + ">[{name}]</> <bold>{message}</>\n{exception}"

logger.add(sys.stderr, format=formatter)
```

```python
def rainbow(text):
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    chars = ("<{}>{}</>".format(colors[i % len(colors)], c) for i, c in enumerate(text))
    return "".join(chars)

def formatter(record):
    rainbow_message = rainbow(record["message"])
    # Prevent '{}' in message (if any) to be incorrectly parsed during formatting
    escaped = rainbow_message.replace("{", "{{").replace("}", "}}")
    return "<b>{time}</> " + escaped + "\n{exception}"

logger.add(sys.stderr, format=formatter)
```

--------------------------------

### Pytest I/O Error on Closed File with Mocked sys.stderr

Source: https://github.com/delgan/loguru/blob/master/docs/resources/troubleshooting.md

This example shows how Loguru can encounter an 'I/O operation on closed file' error within a Pytest environment. It occurs because Pytest's `capsys` fixture mocks `sys.stderr`, and this mock object is closed by Pytest after the test function completes, while the Loguru handler remains active.

```python
import sys
from loguru import logger

logger.remove()

def test_1(capsys):
    # Here, "sys.stderr" is actually a mock object due to usage of "capsys" fixture.
    logger.add(sys.stderr, catch=False)
    logger.info("Test 1")


def test_2():
    # After execution of the previous test, the mocked "sys.stderr" was closed by Pytest.
    # However, the handler was not removed from the Loguru logger. It'll raise a "ValueError" here.
    logger.info("Test 2", catch=False)
```

--------------------------------

### Define and use custom log levels

Source: https://context7.com/delgan/loguru/llms.txt

Create custom levels with specific severity numbers and icons, and optionally add convenience methods.

```python
from loguru import logger

# Add custom level
logger.level("AUDIT", no=35, color="<blue>", icon="📋")
logger.level("NETWORK", no=15, color="<cyan>", icon="🌐")

# Use custom level with log()
logger.log("AUDIT", "User {} performed action {}", "admin", "delete")
logger.log("NETWORK", "Connection established to {}", "api.example.com")

# Retrieve level information
audit_level = logger.level("AUDIT")
print(f"Level: {audit_level.name}, Severity: {audit_level.no}")

# Update existing level properties (cannot change severity 'no')
logger.level("WARNING", icon="⚠️", color="<yellow><bold>")

# Create convenience method for custom level
from functools import partialmethod
logger.__class__.audit = partialmethod(logger.__class__.log, "AUDIT")
logger.audit("Convenient audit logging")

# Configure handler for specific custom level
logger.add("audit.log", filter=lambda r: r["level"].name == "AUDIT")
```

--------------------------------

### Configure Loguru via Environment Variables

Source: https://context7.com/delgan/loguru/llms.txt

Set default logging behavior using shell environment variables.

```bash
# Set default format
export LOGURU_FORMAT="{time} | {level} | {message}"

# Set default level for handlers
export LOGURU_LEVEL="WARNING"

# Customize level colors
export LOGURU_DEBUG_COLOR="<blue>"
export LOGURU_INFO_COLOR="<green>"

# Customize level icons
export LOGURU_ERROR_ICON="X"

# Disable auto-initialization (no default stderr handler)
export LOGURU_AUTOINIT="False"

# Disable colors (NO_COLOR standard)
export NO_COLOR=1

# Force colors even when not a TTY
export FORCE_COLOR=1
```

--------------------------------

### Replace `LoggerAdapter` with `bind()` in Loguru

Source: https://github.com/delgan/loguru/blob/master/docs/resources/migration.md

Instantiate a logger with bound context using `logger.bind(key=value)` for cleaner class integration.

```python
class MyClass:

    def __init__(self, clientip):
        self.logger = logger.bind(clientip=clientip)

    def func(self):
        self.logger.debug("Running func")
```

--------------------------------

### Commit and Push Changes

Source: https://github.com/delgan/loguru/blob/master/docs/project/contributing.md

Commands to stage, commit, and push changes to the remote repository.

```bash
$ git add .
$ git commit -m 'Add succinct explanation of what changed'
$ git push origin fix_bug
```

--------------------------------

### Filter logs using dictionaries and dynamic bindings

Source: https://context7.com/delgan/loguru/llms.txt

Use a dictionary to set per-module log levels or a lambda with bind() for dynamic filtering based on extra context.

```python
level_config = {
    "": "INFO",                # Default level for all modules
    "mypackage.database": "DEBUG",  # More verbose for database
    "noisy_library": "WARNING",     # Less verbose for noisy lib
    "disabled_module": False        # Completely disabled
}
logger.add(sys.stderr, filter=level_config, level=0)

# Dynamic filtering with bind()
logger.add("debug.log", filter=lambda r: r["extra"].get("debug_mode"))

# Enable debug logging for specific operations
debug_logger = logger.bind(debug_mode=True)
debug_logger.debug("This goes to debug.log")
logger.debug("This does not")
```

--------------------------------

### Integrate Loguru with tqdm Progress Bars

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Use `tqdm.write()` instead of direct logging to `sys.stderr` when using Loguru within `tqdm` iterations to avoid disturbing the progress bar display. Consider `colorama.deinit()` if colorization issues arise on Windows with Spyder.

```python
import time

from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)

logger.info("Initializing")

for x in tqdm(range(100)):
    logger.info("Iterating #{}", x)
    time.sleep(0.1)
```

--------------------------------

### Custom Formatter for Single-Line Logs

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Use a custom formatter with `bind()` and `opt()` to write multiple log messages on the same line. This is useful for showing step-by-step progress.

```python
def formatter(record):
    end = record["extra"].get("end", "\n")
    return "[{time}] {message}" + end + "{exception}"

logger.add(sys.stderr, format=formatter)
logger.add("foo.log", mode="w")

logger.bind(end="").debug("Progress: ")

for _ in range(5):
    logger.opt(raw=True).debug(".")

logger.opt(raw=True).debug("\n")

logger.info("Done")
```

--------------------------------

### Restricting Log File Permissions

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Use a custom opener function with os.open to enforce specific file permissions, such as 0o600, when creating log files.

```python
def opener(file, flags):
    return os.open(file, flags, 0o600)

logger.add("combined.log", opener=opener)
```

--------------------------------

### Adding a Sink

Source: https://github.com/delgan/loguru/blob/master/docs/api/logger.md

This section details how to add a sink to the logger, including available parameters and return values.

```APIDOC
## POST /api/loguru/add

### Description
Adds a new sink to the logger instance.

### Method
POST

### Endpoint
/api/loguru/add

### Parameters
#### Query Parameters
- **mode** (str, optional) - The opening mode as for built-in `open()` function. It defaults to "a" (open the file in appending mode).
- **buffering** (int, optional) - The buffering policy as for built-in `open()` function. It defaults to `1` (line buffered file).
- **encoding** (str, optional) - The file encoding as for built-in `open()` function. It defaults to "utf8".
- **kwargs** - Others parameters are passed to the built-in `open()` function.

### Request Body
- **sink** (Union[str, pathlib.Path, file-like object, callable, coroutine function, logging.Handler]) - The sink to add. Can be a file path, a file-like object, a callable, a coroutine function, or a built-in `logging.Handler`.
- **format** (str or callable, optional) - The format string or function for log messages. Defaults to a standard format.
- **filter** (str, dict, callable, optional) - The filter to apply to log messages. Can be a string, a dictionary, or a callable.
- **level** (str or int, optional) - The minimum level for messages to be logged by this sink.

### Response
#### Success Response (200)
- **id** (int) - An identifier associated with the added sink, used for removal.

#### Error Response (400)
- **error** (str) - Description of the error if any arguments are invalid.

### Raises
**ValueError** - If any of the arguments passed to configure the sink is invalid.
```

--------------------------------

### Implement function entry and exit logging with a decorator

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Uses a decorator to log function arguments and return values. Requires functools and the loguru logger.

```python
import functools
from loguru import logger


def logger_wraps(*, entry=True, exit=True, level="DEBUG"):

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper
```

```python
@logger_wraps()
def foo(a, b, c):
    logger.info("Inside the function")
    return a * b * c

def bar():
    foo(2, 4, c=8)

bar()
```

--------------------------------

### Configuring Loguru for Linux multiprocessing

Source: https://github.com/delgan/loguru/blob/master/docs/resources/recipes.md

Use the enqueue=True parameter to safely handle concurrent access to sinks in child processes on Linux.

```python
# Linux implementation
import multiprocessing
from loguru import logger

def my_process():
    logger.info("Executing function in child process")
    logger.complete()

if __name__ == "__main__":
    logger.add("file.log", enqueue=True)

    process = multiprocessing.Process(target=my_process)
    process.start()
    process.join()

    logger.info("Done")
```

