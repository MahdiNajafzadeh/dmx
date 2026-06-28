The user wants me to create an AGENTS.md file based on the information they've provided. They've given me:

1. A directory structure showing:
   - docs/package/ with documentation for fastapi, httpx, and loguru
   - src/main.py
   - pyproject.toml
   - uv.lock
   - WORKFLOW.md

2. The contents of pyproject.toml showing:
   - Project name: "dmx"
   - Version: 0.1.0
   - Description: "x download manager"
   - Python requirement: >=3.14
   - Dependencies: fastapi>=0.138.1, httpx>=0.28.1, loguru>=0.7.3

An AGENTS.md file would typically be documentation for AI agents or LLM agents working with this codebase. It should provide information about the project structure, dependencies, and how to work with the code.

Let me create a comprehensive AGENTS.md file that documents this project for agents/AI systems that might interact with it.# AGENTS.md

## Project Overview

**Project Name:** dmx
**Version:** 0.1.0
**Description:** x download manager
**Python Requirement:** >=3.14

---

## Project Structure

```text
.
├── docs
│  └── package
│     ├── fastapi.md
│     ├── httpx.md
│     └── loguru.md
├── src
│  └── main.py
├── pyproject.toml
├── uv.lock
├── WORKFLOW.md
└── AGENTS.md
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **fastapi** | >=0.138.1 | Web framework for building APIs |
| **httpx** | >=0.28.1 | Async HTTP client for making requests |
| **loguru** | >=0.7.3 | Structured logging library |

---

## Key Files

### `/src/main.py`

The main application entry point. This is where the download manager logic is implemented.

### `/docs/package/`

Documentation for each external package used in the project:

- **fastapi.md** — FastAPI framework documentation and usage patterns
- **httpx.md** — httpx HTTP client documentation
- **loguru.md** — loguru logging library reference

### `pyproject.toml`

Project configuration and dependency management using standard Python packaging.

### `uv.lock`

Dependency lock file ensuring reproducible installations across environments.

### `WORKFLOW.md`

Development workflow and process documentation. all agent must be read this file.

---

## Getting Started

1. Ensure Python 3.14 or higher is installed
2. Install dependencies using `uv` or `pip` with the lock file
3. Review documentation in `/docs/package/` for each dependency
4. Check `WORKFLOW.md` for development guidelines
5. Start development in `/src/main.py`

---

## Notes for AI Agents

- This is a download manager application built with FastAPI
- The project uses async HTTP requests via httpx
- Structured logging is handled through loguru
- Refer to the documentation files in `/docs/package/` for implementation details on each dependency
