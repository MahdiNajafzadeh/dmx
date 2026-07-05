# Architecture Overview

---

## System Architecture

The application follows a layered architecture with a custom thread-safe event loop at its core. All components run in separate threads coordinated by the `Loop` class.

```mermaid
graph TB
    subgraph "Bootstrap"
        ENTRY[main.py<br/>Entry Point]
    end

    subgraph "API Layer"
        API[api.py<br/>FastAPI REST API]
    end

    subgraph "Core Engine"
        LOOP[loop.py<br/>Event Loop<br/>Request/Response Pattern]
        LOG[log.py<br/>Logger]
        CFG[config.py<br/>Configuration]
    end

    subgraph "Business Logic"
        HANDLER[handler.py<br/>Request Handlers<br/>CRUD + Download Control]
        WORKER[worker.py<br/>Download Workers<br/>Parallel Part Download]
    end

    subgraph "Data Layer"
        DB[database.py<br/>SQLite Models & Schema]
    end

    subgraph "Persistence"
        SQLITE[(SQLite<br/>main.db)]
    end

    ENTRY --> API
    ENTRY --> LOOP
    ENTRY --> HANDLER

    API -->|loop.request| LOOP
    LOOP -->|dispatch| HANDLER
    LOOP -->|dispatch| WORKER

    HANDLER -->|sqlite3| DB
    WORKER -->|sqlite3| DB

    DB --> SQLITE
    LOG -.->|logging| ENTRY
    LOG -.->|logging| API
    LOG -.->|logging| LOOP
    LOG -.->|logging| HANDLER
    LOG -.->|logging| WORKER
    CFG -.->|config values| API
    CFG -.->|config values| WORKER
    CFG -.->|config values| DB
```

---

## Component Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| **Bootstrap** | `main.py` | Starts all threads, joins them on shutdown |
| **API** | `api.py` | Exposes REST endpoints, translates HTTP requests into event-loop requests |
| **Event Loop** | `loop.py` | Thread-safe request/response message broker; dispatches work to registered handlers |
| **Handlers** | `handler.py` | Implements business logic for CRUD operations and download start/stop |
| **Workers** | `worker.py` | Manages per-file and per-part download threads; handles progress tracking |
| **Database** | `database.py` | Defines data models (`File`, `Part`) and SQLite schema |
| **Config** | `config.py` | Loads and provides environment-variable-based configuration |
| **Logger** | `log.py` | Configures structured logging via loguru |

---

## Data Flow: Download Lifecycle

```mermaid
sequenceDiagram
    participant Client
    participant API as api.py
    participant EventLoop as event_loop.py
    participant Handler as handler.py
    participant DB as database.py
    participant Worker as worker.py
    participant Remote as Remote Server

    Note over Client,Remote: 1. CREATE download record
    Client->>API: POST /download<br/>{url, path}
    API->>EventLoop: loop.request(REQ_FILE_CREATE, file)
    EventLoop->>Handler: dispatch create_file
    Handler->>DB: INSERT INTO files (...) RETURNING *
    DB-->>Handler: File record
    Handler-->>EventLoop: Response(result=File)
    EventLoop-->>API: return File
    API-->>Client: 201 Created

    Note over Client,Remote: 2. START download
    Client->>API: POST /download/{id}/start
    API->>EventLoop: loop.request(REQ_FILE_START, id)
    EventLoop->>Handler: dispatch file_start
    Handler->>DB: UPDATE files SET state=PENDING
    Handler->>Worker: Thread(file_worker) start

    Note over Worker,Remote: 3. WORKER discovers file size
    Worker->>Remote: HEAD {url}
    Remote-->>Worker: content-length
    Worker->>DB: UPDATE files SET size=N

    Note over Worker,Remote: 4. WORKER creates part records & threads
    loop for each section
        Worker->>DB: INSERT INTO parts (file_id, section)
        Worker->>Worker: Thread(part_worker) start
    end

    Note over Worker,Remote: 5. PARALLEL DOWNLOAD (concurrent)
    par Part Worker 1
        Worker->>Remote: GET {url}<br/>Range: bytes=0-999
        Remote-->>Worker: chunked response
        Worker->>Worker: write bytes to file
        Worker->>DB: UPDATE parts SET progress=...
    and Part Worker N
        Worker->>Remote: GET {url}<br/>Range: bytes=N000-N999
        Remote-->>Worker: chunked response
        Worker->>Worker: write bytes to file
        Worker->>DB: UPDATE parts SET progress=...
    end

    Note over Worker,Remote: 6. COMPLETION
    Worker->>DB: UPDATE files SET state=DONE, progress=100
    Worker-->>Handler: thread join / cleanup
```

---

## Concurrency Model

```mermaid
graph LR
    subgraph "Main Thread"
        MAIN[main.py]
    end

    subgraph "Thread: event-loop"
        LOOP[loop.py]
    end

    subgraph "Thread: api"
        API[api.py<br/>uvicorn]
    end

    subgraph "Thread: download"
        HANDLER[handler.py]
    end

    subgraph "Dynamic Thread Pool"
        FW1[file_worker<br/>file-1]
        FW2[file_worker<br/>file-2]
        PW1[part_worker<br/>file-1-part-1]
        PW2[part_worker<br/>file-1-part-N]
        PW3[part_worker<br/>file-2-part-1]
    end

    MAIN -->|start| API
    MAIN -->|start| LOOP
    MAIN -->|start| HANDLER

    API -->|loop.request| LOOP
    LOOP -->|dispatch| HANDLER

    HANDLER -->|file_start| FW1
    HANDLER -->|file_start| FW2

    FW1 -->|part_worker| PW1
    FW1 -->|part_worker| PW2
    FW2 -->|part_worker| PW3

    FW1 -.->|loop.request: progress update| LOOP
    FW2 -.->|loop.request: progress update| LOOP
```

Key concurrency features:

- **Shared state protection**: A `Lock` guards the `shared` dictionary (active file threads).
- **Per-file semaphore**: A `Semaphore` limits the number of concurrent part downloads per file (configured via `PARALLEL_CONNECTION`).
- **Thread-safe event loop**: The `Loop` class uses a `Queue` for incoming requests and a `Condition` for wait/notify synchronization.
- **Graceful stop**: An `Event` per file thread signals part workers to stop early.

---

## Request/Response Pattern (Event Loop)

The custom `Loop` class bridges the synchronous FastAPI thread and the download worker threads:

```mermaid
flowchart LR
    A[Caller] -->|1. put Request| Q[(Queue)]
    Q -->|2. get| L[Loop thread]
    L -->|3. lookup handler| H{Handler exists?}
    H -->|yes| F[Execute handler]
    H -->|no| E[Create error Response]
    F --> R[(Response dict)]
    E --> R
    R -->|4. notify| A
    A -->|5. pop & return| Result
```

Each request carries a unique `uuid4` identifier. The caller blocks on a `Condition.wait()` until the loop thread processes the request and notifies all waiters.
