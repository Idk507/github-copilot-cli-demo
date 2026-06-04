from fastapi import APIRouter, HTTPException, status

from models import Task, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks: list[Task] = []


@router.get("", response_model=list[Task])
def get_tasks() -> list[Task]:
    """Return all tasks."""
    return tasks


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    """Create a new task with an auto-incremented ID."""
    next_id = tasks[-1].id + 1 if tasks else 1
    new_task = Task(id=next_id, **task.model_dump())
    tasks.append(new_task)
    return new_task


@router.get(r"/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    """Return a single task by ID."""
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.delete(r"/{task_id}", response_model=Task)
def delete_task(task_id: int) -> Task:
    """Delete a single task by ID."""
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(index)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
