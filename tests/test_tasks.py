import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from routes.tasks import tasks


@pytest.fixture(autouse=True)
def clear_tasks() -> None:
    tasks.clear()


@pytest.mark.anyio
async def test_get_tasks_returns_empty_list() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_create_task_assigns_incrementing_ids() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        first_response = await client.post(
            "/tasks",
            json={"title": "First task", "description": "First description"},
        )
        second_response = await client.post(
            "/tasks",
            json={"title": "Second task", "description": "Second description"},
        )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["id"] == 1
    assert second_response.json()["id"] == 2


@pytest.mark.anyio
async def test_get_task_returns_existing_task() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_response = await client.post(
            "/tasks",
            json={"title": "Read docs", "description": "Review the API docs"},
        )
        task_id = create_response.json()["id"]
        response = await client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "Read docs",
        "description": "Review the API docs",
        "done": False,
    }


@pytest.mark.anyio
async def test_delete_task_removes_existing_task() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_response = await client.post(
            "/tasks",
            json={"title": "Clean up", "description": "Delete finished work"},
        )
        task_id = create_response.json()["id"]
        delete_response = await client.delete(f"/tasks/{task_id}")
        list_response = await client.get("/tasks")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == task_id
    assert list_response.json() == []


@pytest.mark.anyio
async def test_missing_task_returns_404() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
