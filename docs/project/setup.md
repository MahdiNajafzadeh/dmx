# Setup & Running

## Prerequisites

- **Python** >=3.14
- **uv** (recommended) or **pip** for dependency management

---

## Installation

### Using uv (recommended)

```shell
# Clone the repository
git clone <repo-url> && cd dmx

# Create a virtual environment and install dependencies
uv sync

# Activate the environment
source .venv/bin/activate
```

### Using pip

```shell
python3.14 -m venv .venv
source .venv/bin/activate
pip install fastapi>=0.138.1 httpx>=0.28.1 loguru>=0.7.3 python-dotenv>=1.2.2 uvicorn>=0.49.0
```

---

## Configuration

The application reads configuration from environment variables. A `.env` file in the project root is loaded automatically if present.

| Variable | Default | Description |
|----------|---------|-------------|
| `PARALLEL_DOWNLOAD` | `2` | Maximum number of files downloaded simultaneously |
| `PARALLEL_CONNECTION` | `8` | Number of concurrent byte-range connections per file |
| `DATABASE_PATH` | `main.db` | Path to the SQLite database file |
| `HOST` | `0.0.0.0` | API server bind address |
| `PORT` | `3000` | API server port |

### Example `.env`

```ini
PARALLEL_DOWNLOAD=4
PARALLEL_CONNECTION=16
DATABASE_PATH=/data/dmx.db
HOST=127.0.0.1
PORT=8080
```

---

## Running the Application

```shell
# From the project root
python src/main.py
```

This starts three threads concurrently:

1. **Event loop** — processes internal request/response messages
2. **API server** — uvicorn serving the FastAPI app
3. **Download handlers** — ready to accept download start/stop commands

The API is available at `http://<HOST>:<PORT>` (default `http://0.0.0.0:3000`).

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/download` | List all downloads |
| `GET` | `/download/{id}` | Get a single download record |
| `POST` | `/download` | Create a new download (body: `File` JSON) |
| `PATCH` | `/download/{id}` | Update a download record |
| `DELETE` | `/download/{id}` | Delete a download record |
| `POST` | `/download/{id}/start` | Start downloading a file |
| `POST` | `/download/{id}/stop` | Stop an active download |

### Example: Create and start a download

```shell
# Create a download record
curl -X POST http://localhost:3000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/file.zip", "path": "/tmp/file.zip"}'

# Start the download (replace {id} with the returned id)
curl -X POST http://localhost:3000/download/1/start

# Check progress
curl http://localhost:3000/download/1
```

---

## Database

The application uses SQLite with Write-Ahead Logging (WAL) mode. Two tables are created automatically on first run:

- **files** — download file records (url, path, size, state, progress)
- **parts** — byte-range section records per file (file_id, section, size, state, progress)

The database file location is controlled by the `DATABASE_PATH` environment variable.

---

## Verification

```shell
# Check that the server is running
curl http://localhost:3000/download

# Expected: [] (empty list) or existing download records
```
