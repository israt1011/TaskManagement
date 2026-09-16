from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Management API")


# Task model
class Task(BaseModel):
    id: int | None = None
    title: str
    description: str
    status: str
    priority: str


# In-memory database
tasks = {}
next_id = 1


# GET - Get all tasks
@app.get("/tasks")
def get_tasks():
    return list(tasks.values())


# GET - Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return tasks[task_id]


# POST - Create a task
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global next_id

    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority
    }

    tasks[next_id] = new_task
    next_id += 1

    return new_task


# PUT - Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority
    }

    tasks[task_id] = updated_task

    return updated_task


# DELETE - Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = tasks.pop(task_id)

    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }