## **Project Brief**

**Implement a multi-threaded Python download manager** with manual event-loop coordination, SQLite persistence, and FastAPI REST interface. The system uses a custom request-handler loop to orchestrate concurrent file and part downloads across multiple worker threads.

---

## **System Architecture**

| Component | Responsibility | Location |
|-----------|-----------------|----------|
| **Loop (Event-Loop)** | Request registry, handler dispatch, response routing | `src/loop.py` |
| **File-Thread** | Download orchestration, part coordination, progress aggregation | `src/download.py` |
| **Part-Thread** | Chunk-level HTTP download with Range requests | `src/download.py` |
| **REST API** | HTTP interface mapping endpoints to Loop requests | `src/api.py` |
| **Database** | SQLite persistence for files, parts, status, progress | `src/database.py` |
| **Logging** | Structured logging using loguru | `src/log.py` |
| **Bootstrap** | Main entry point initialization | `src/main.py` |

---

## **Core Workflows**

### **Loop Mechanism (Event-Driven Dispatch)**

The Loop acts as a **message broker** for internal system requests:

- **Code Enum**: 14 request types identifying handler targets
- **Decorator-Based Registry**: `@loop.handler(Code.REQ_*)` registers request handlers
- **Queue-Based I/O**: Thread-safe queue for inter-thread communication
- **Response Mapping**: UUID-keyed Dict[UUID, Any] for async response collection
- **Condition Variable**: Notifies waiting threads when responses arrive

### **File-Thread Workflow (Download Job)**

1. Triggered by **REQ_FILE_START(file_id)**
2. Fetch file metadata from DB (url, path)
3. Issue HEAD request → retrieve Content-Length
4. Update DB with file size via **REQ_FILE_UPDATE**
5. Create 8 Part-Threads via **REQ_PART_START** calls
6. Listen for progress updates from Part-Threads
7. Persist progress to DB via **REQ_PART_UPDATE**
8. Once all parts complete: merge chunks → finalize file → update DB status to DONE

### **Part-Thread Workflow (Chunk Download)**

1. Triggered by **REQ_PART_START(file_id, part_id)**
2. Validate identifiers via **REQ_PART_GET(file_id, part_id)**
3. HTTP GET with Range header → download assigned byte range
4. After each write: emit progress via **REQ_PART_UPDATE(part_id, progress)**
5. Persist status (DONE/ERROR) to DB
6. Report completion to parent File-Thread

### **Thread Hierarchy**

```text
Main Thread
  ├─ File-Thread (Download Job 1)
  │   ├─ Part-Thread 1 (bytes 0-chunk_size)
  │   ├─ Part-Thread 2 (bytes chunk_size-2*chunk_size)
  │   └─ Part-Thread 8 (bytes 7*chunk_size-end)
  ├─ File-Thread (Download Job 2)
  │   ├─ Part-Thread 1
  │   └─ Part-Thread 8
  └─ ...File-Thread N
```

---

## **Request Handler Definitions**

### **File Operations**

- `REQ_FILE_GET_ALL()` → `List[File]`
- `REQ_FILE_GET(id: int)` → `File | None`
- `REQ_FILE_CREATE(file: File)` → `None`
- `REQ_FILE_UPDATE(id: int, file: File)` → `File | None`
- `REQ_FILE_START(id: int)` → `None` (spawn File-Thread)
- `REQ_FILE_PAUSE(id: int)` → `None` (gracefully stop File-Thread + child Part-Threads)
- `REQ_FILE_REMOVE(id: int)` → `File | None` (requires file in paused/error state)

### **Part Operations**

- `REQ_PART_GET_ALL(file_id: int)` → `List[Part] | None`
- `REQ_PART_GET(file_id: int, id: int)` → `Part | None`
- `REQ_PART_CREATE(part: Part)` → `None`
- `REQ_PART_UPDATE(id: int, part: Part)` → `Part | None` (progress sync)
- `REQ_PART_START(file_id: int, id: int)` → `None` (spawn Part-Thread)
- `REQ_PART_PAUSE(id: int)` → `None`
- `REQ_PART_REMOVE(id: int)` → `Part | None`

---

## **Data Model**

### **File Record**

```python
class Status(Enum):
   PENDING = "pending"
   ERROR = "error"
   DONE = "done"
   PAUSE = "pause"

class File:
	id: int                # Primary key
	url: str              # Source URL
	path: str             # Destination path
	size: int             # Total file size (bytes)
	status: Status        # Current state
	progress: int         # Bytes downloaded
```

### **Part Record**

```python
class Part:
	id: int               # Primary key
	file_id: int          # Foreign key (files.id)
	section: int          # Chunk index (0-7 for 8 parts)
	status: Status        # Current state
	progress: int         # Bytes downloaded in this chunk
```

---

## **REST API Routes**

| Method | Endpoint | Mapped Request |
|--------|----------|--------|
| GET | `/download` | `REQ_FILE_GET_ALL()` |
| GET | `/download/{id}` | `REQ_FILE_GET(id)` |
| POST | `/download` | `REQ_FILE_CREATE(file)` |
| PATCH | `/download/{id}` | `REQ_FILE_UPDATE(id, file)` |
| DELETE | `/download/{id}` | `REQ_FILE_REMOVE(id)` |
| POST | `/download/{id}/start` | `REQ_FILE_START(id)` |
| POST | `/download/{id}/pause` | `REQ_FILE_PAUSE(id)` |

---

## **Shared State Management**

**File and Part threads must be tracked via shared state:**

```python
class PartThread:
	id: int
	file_id: int
	thread: threading.Thread

class FileThread:
	id: int
	thread: threading.Thread
	parts: dict[int, PartThread]

# Global shared state
file_threads: dict[int, FileThread]        # Key: file_id
part_threads: dict[str, PartThread]        # Key: "{file_id}:{part_id}"
```

**Pause Mechanics:**

1. File-Thread receives pause signal
2. File-Thread notifies all child Part-Threads
3. Part-Threads exit gracefully and are removed from `part_threads`
4. File-Thread is removed from `file_threads`
5. DB status updated to PAUSE

---

## **Implementation Constraints**

1. **Database Synchronization**: All state changes must persist to DB immediately (transactional guarantees recommended)
2. **File Creation**: New files created via API must default to PENDING status and require explicit `POST /download/{id}/start` to begin
3. **File Deletion**: Only allowed if file status is PAUSE or ERROR
4. **Part Thread Count**: Fixed at 8 concurrent parts per file download
5. **Progress Tracking**: Part-Thread must update DB after each successful write to ensure recovery on crashes
6. **Thread Cleanup**: All spawned threads must be tracked and explicitly joined on shutdown

---

## **Dependencies**

- **fastapi** — REST API framework
- **loguru** — Structured logging
- **httpx** — HTTP client (Range requests, HEAD requests)
- **sqlite3** — Standard library (bundled)
- **threading** — Standard library (bundled)

---

## **Agent Orchestration Flags**

```text
orchestrator-flags: +use_multi_agent +use_parallel_agent +use_duplicate_agent
```

**Recommended Agent Delegation:**

| Agent Role | Responsibility | Parallelization |
|-----------|-----------------|-----------------|
| **Loop-Agent** | Implement event-loop, handler registry, request dispatch | Sequential (single loop) |
| **Database-Agent** | SQLite schema, CRUD ops, transaction handling | Sequential (serialized) |
| **File-Handler Agent** | File-Thread logic, part coordination, chunk merging | Parallel (per file) |
| **Part-Handler Agent** | Part-Thread logic, HTTP Range requests, progress sync | Parallel (per part, up to 8 concurrent per file) |
| **API-Agent** | REST endpoints, request validation, response formatting | Parallel (via FastAPI) |
| **Logger-Agent** | Centralized loguru configuration, formatted output | Shared (non-blocking) |

---

## **Success Criteria**

✅ Loop correctly dispatches all 14 request types
✅ File download creates exactly 8 Part-Threads
✅ Progress updates persist to DB in real-time
✅ Pause operation gracefully terminates threads and cleans shared state
✅ File merging produces valid output file
✅ All 7 API endpoints function correctly
✅ No race conditions in shared state access (use locks if needed)
✅ Concurrent downloads do not interfere with each other
