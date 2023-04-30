import pytest
from fastapi.testclient import TestClient
from app import main
from app import config

main.settings = config.Settings(_env_file="test.env") # type: ignore

def test_create():
    with TestClient(main.app) as client:
        test_tasks = [
            {"name": "Test task 1", "deadline": "2024-01-01"},
            {"name": "Another task"},
            {"name": "Just one more", "deadline": "2025-02-17"},
            {"name": "The last one"},
        ]

        for task in test_tasks:
            # create task
            response = client.post("/tasks", json=task)
            assert response.status_code == 200
            assert response.json().get("id") is not None
            assert response.json().get("name") == task["name"]
            assert response.json().get("deadline", None) == task.get("deadline", None)

            id = response.json().get("id")

            # read the same task from api
            response = client.get(f"/tasks/id/{id}")
            assert response.status_code == 200
            assert response.json().get("name") == task["name"]
            assert response.json().get("deadline", None) == task.get("deadline", None)
            assert response.json().get("finished") == False
