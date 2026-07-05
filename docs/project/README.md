# dmx — x Download Manager

**Version:** 0.1.0  
**Python:** >=3.14  
**Description:** A multi-threaded parallel file download manager with a FastAPI REST API.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Documentation Map](#documentation-map)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)

---

## Overview

`dmx` is a download manager that splits files into byte-range sections and downloads them concurrently using multiple worker threads. It exposes a REST API via FastAPI for creating, monitoring, and controlling downloads, and uses SQLite for persistent state tracking.

The system is composed of three major layers:

1. **API Layer** — FastAPI REST endpoints for client interaction
2. **Core Engine** — A custom thread-safe event loop that routes requests to registered handlers
3. **Worker Layer** — A thread pool that handles parallel file/part downloads with progress tracking

All components are bootstrapped by a single entry point and run concurrently via dedicated threads.

---

## Quick Start

```shell
# Ensure Python 3.14+ is installed
python --version

# Install dependencies
uv sync
# or: pip install -r <(uv export --format requirements)

# (Optional) Create a .env file to override defaults:
#   PARALLEL_DOWNLOAD=2
#   PARALLEL_CONNECTION=8
#   DATABASE_PATH=main.db
#   HOST=0.0.0.0
#   PORT=3000

# Run the application
python src/main.py
```

The API server starts on `http://0.0.0.0:3000` by default.

---

## Documentation Map

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file — project overview and index |
| [setup.md](setup.md) | Detailed setup, configuration, and running instructions |
| [architecture.md](architecture.md) | High-level architecture with Mermaid diagrams |
| [modules.md](modules.md) | Catalog of all Python modules with extracted descriptions |

---

## Project Structure

```text
.
├── docs/
│   ├── package/          # Third-party library reference docs
│   │   ├── fastapi.md
│   │   ├── httpx.md
│   │   └── loguru.md
│   └── project/          # Project documentation (this directory)
│       ├── README.md
│       ├── setup.md
│       ├── architecture.md
│       └── modules.md
├── src/
│   ├── main.py           # Entry point / bootstrap
│   ├── api.py            # FastAPI REST endpoints
│   ├── config.py         # Environment-based configuration
│   ├── database.py       # SQLite models and schema
│   ├── handler.py        # Request handlers (CRUD + download control)
│   ├── log.py            # Loguru logger initialisation
│   ├── loop.py           # Custom event loop (request/response pattern)
│   └── worker.py         # Parallel download worker threads
├── pyproject.toml        # Project metadata and dependencies
├── uv.lock               # Reproducible dependency lock file
├── WORKFLOW.md           # Multi-agent CI/CD workflow definition
└── AGENTS.md             # AI agent instructions for this codebase
```

---

## Technology Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Web framework | **FastAPI** >=0.138.1 | REST API endpoints |
| ASGI server | **uvicorn** >=0.49.0 | HTTP server |
| HTTP client | **httpx** >=0.28.1 | Outbound requests for file downloads |
| Logging | **loguru** >=0.7.3 | Structured logging |
| Database | **SQLite** (stdlib) | Persistent download state |
| Configuration | **python-dotenv** >=1.2.2 | `.env` file loading |
| Concurrency | **threading** (stdlib) | Parallel workers |
| Packaging | **uv** | Dependency & environment management |
