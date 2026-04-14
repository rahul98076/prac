# Demo API

A basic Flask REST API for managing server inventory.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed
- Python 3.12 or higher

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

## Running the Application

To start the server, run:
```bash
uv run app.py
```
The server will start on `http://localhost:5000`.

## Endpoints

### Base & Health
- `GET /` : Returns a welcome message.
- `GET /health` : Returns the health status of the API.

### Servers
- `GET /servers` : Returns a list of all servers.
- `GET /servers/<int:server_id>` : Returns a specific server by ID.
- `POST /servers` : Creates a new server.
  - Requires JSON payload with a `name` field. Optional `role` field.
  - Example: `{"name": "web-server-02", "role": "frontend"}`
- `PUT /servers/<int:server_id>` : Updates an existing server's properties.
  - Accepts JSON payload with `name` and/or `role`.
- `DELETE /servers/<int:server_id>` : Deletes a server by ID.

## Running Tests

To run the test suite using pytest:
```bash
uv run pytest
```

