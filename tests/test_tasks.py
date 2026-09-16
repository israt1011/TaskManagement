import pytest
from fastapi.testclient import TestClient
import main


client = TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_tasks():
    main.tasks.clear()
    main.next_id = 1


# -------------------------
# GET TESTS
# -------------------------

def test_get_tasks_empty():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


# -------------------------
# POST TEST
# -------------------------

def test_create_task():
    task = {
        "title": "Learn FastAPI",
        "description": "Learn FastAPI basics",
        "status": "pending",
        "priority": "high"
    }

    response = client.post("/tasks", json=task)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Learn FastAPI basics"
    assert data["status"] == "pending"
    assert data["priority"] == "high"


# -------------------------
# GET ONE TASK
# -------------------------

def test_get_task():
    task = {
        "title": "Learn Python",
        "description": "Practice Python",
        "status": "pending",
        "priority": "medium"
    }

    client.post("/tasks", json=task)

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Learn Python"


# -------------------------
# PUT TEST
# -------------------------

def test_update_task():
    task = {
        "title": "Learn Python",
        "description": "Practice Python",
        "status": "pending",
        "priority": "medium"
    }

    client.post("/tasks", json=task)

    updated_task = {
        "title": "Learn Advanced Python",
        "description": "Practice advanced Python",
        "status": "completed",
        "priority": "high"
    }

    response = client.put("/tasks/1", json=updated_task)

    assert response.status_code == 200
    assert response.json()["title"] == "Learn Advanced Python"
    assert response.json()["status"] == "completed"


# -------------------------
# DELETE TEST
# -------------------------

def test_delete_task():
    task = {
        "title": "Temporary Task",
        "description": "This task will be deleted",
        "status": "pending",
        "priority": "low"
    }

    client.post("/tasks", json=task)

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    # Confirm task no longer exists
    get_response = client.get("/tasks/1")

    assert get_response.status_code == 404


# -------------------------
# INVALID SCENARIO 1
# -------------------------

def test_create_task_without_title():
    task = {
        "description": "Task without title",
        "status": "pending",
        "priority": "high"
    }

    response = client.post("/tasks", json=task)

    assert response.status_code == 422


# -------------------------
# INVALID SCENARIO 2
# -------------------------

def test_get_nonexistent_task():
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# -------------------------
# INVALID SCENARIO 3
# -------------------------

def test_update_nonexistent_task():
    task = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": "completed",
        "priority": "high"
    }

    response = client.put("/tasks/999", json=task)

    assert response.status_code == 404


# -------------------------
# INVALID SCENARIO 4
# -------------------------

def test_delete_nonexistent_task():
    response = client.delete("/tasks/999")

    assert response.status_code == 404