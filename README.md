# dmx

<p align="center">
  <strong>Multi-threaded parallel file download manager with a FastAPI REST API</strong>
</p>

<p align="center">
  
![Python](https://img.shields.io/badge/Python-≥3.14-blue.svg)
![Version](https://img.shields.io/badge/Version-0.1.0-orange.svg)
![Status](https://img.shields.io/badge/Status-Early%20Development-yellow.svg)

![FastAPI](https://img.shields.io/badge/FastAPI-≥0.138.1-green.svg)
![httpx](https://img.shields.io/badge/httpx-≥0.28.1-blue.svg)
![loguru](https://img.shields.io/badge/loguru-≥0.7.3-blueviolet.svg)

</p>

---

**dmx** is a high-performance file download manager that splits files into byte-range sections and downloads them in parallel using multiple worker threads. It exposes a clean REST API for creating, monitoring, and controlling downloads programmatically.

## Key Features

- **Parallel Downloads** — Files split into sections and downloaded concurrently
- **Progress Tracking** — Real-time progress reporting per part and overall
- **Start/Stop Control** — Dynamically start, stop, and resume downloads
- **REST API** — Full CRUD operations via FastAPI endpoints
- **Persistent State** — SQLite-backed download history and tracking
- **Thread-Safe Architecture** — Custom event loop with request/response routing

## Quick Facts

| | |
|---|---|
| **Max Simultaneous Downloads** | Configurable (default: 2) |
| **Connections Per File** | Configurable (default: 8) |
| **Persistence** | SQLite |
| **API Port** | 3000 (default) |

## Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/dmx.git
cd dmx

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

## Quick Start

```bash
# Start the server
uv run python src/main.py
```

### Create a Download

```bash
curl -X POST http://localhost:3000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/file.zip", "filename": "file.zip"}'
```

### Start Downloading

```bash
curl -X POST http://localhost:3000/download/1/start
```

### Monitor Progress

```bash
curl http://localhost:3000/download/1
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/download` | List all downloads |
| `GET` | `/download/{id}` | Get download details |
| `POST` | `/download` | Create new download |
| `PATCH` | `/download/{id}` | Update download |
| `DELETE` | `/download/{id}` | Delete download |
| `POST` | `/download/{id}/start` | Start downloading |
| `POST` | `/download/{id}/stop` | Stop download |

For complete documentation, see [`docs/project/`](docs/project/).

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PARALLEL_DOWNLOAD` | 2 | Max simultaneous file downloads |
| `PARALLEL_CONNECTION` | 8 | Concurrent connections per file |
| `DATABASE_PATH` | main.db | SQLite database path |
| `HOST` | 0.0.0.0 | API bind address |
| `PORT` | 3000 | API port |

## Project Structure

```
src/
├── main.py      # Entry point, bootstraps threads
├── api.py       # FastAPI REST endpoints
├── loop.py      # Thread-safe event loop
├── handler.py   # Request handlers
├── worker.py    # Parallel download workers
├── database.py  # SQLite models
├── config.py    # Configuration loader
└── log.py       # Loguru logger
```

## Contributing

See [WORKFLOW.md](WORKFLOW.md) for the multi-agent development workflow. Contributions follow a structured review process:

1. **Developer** → Code generation
2. **Reviewer** → Quality gate
3. **Tester** → Verification
4. **Version Control** → Dependency validation

## License

Not yet specified.

## Author

dmx Development Team
