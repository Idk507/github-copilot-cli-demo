# FastAPI Task Manager

A simple FastAPI REST API for managing tasks in memory. The project exposes CRUD-style task endpoints under `/tasks` and uses Pydantic models for request and response validation.

## Features

- FastAPI application entry point in `main.py`
- Pydantic task models in `models.py`
- Task routes in `routes/tasks.py`
- In-memory task storage with auto-incrementing IDs

## Requirements

- Python 3.11+

Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running the API

Start the development server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

## Data Models

### Task

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "done": false
}
```

### TaskCreate

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "done": false
}
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/tasks` | Return all tasks |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/{task_id}` | Return one task by ID |
| DELETE | `/tasks/{task_id}` | Delete one task by ID |

### GET /tasks

Returns the full task list.

```bash
curl http://127.0.0.1:8000/tasks
```

Example response:

```json
[]
```

### POST /tasks

Creates a task and assigns the next available integer ID.

```bash
curl -X POST http://127.0.0.1:8000/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Buy groceries\",\"description\":\"Milk, eggs, and bread\",\"done\":false}"
```

Example response:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "done": false
}
```

### GET /tasks/{task_id}

Returns a single task when it exists.

```bash
curl http://127.0.0.1:8000/tasks/1
```

Example response:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "done": false
}
```

If the task does not exist:

```json
{
  "detail": "Task not found"
}
```

### DELETE /tasks/{task_id}

Deletes a task and returns the deleted object.

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

Example response:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "done": false
}
```

If the task does not exist:

```json
{
  "detail": "Task not found"
}
```
