import pytest
from fastapi.testclient import TestClient
from app import main
from app import config

main.settings = config.Settings(_env_file="test.env") # type: ignore

def test_fetch_all():
    with TestClient(main.app) as client:
        test_tasks = [
            {"name": "Test task 1", "deadline": "2024-01-01"},
            {"name": "Another task"},
            {"name": "Just one more", "deadline": "2025-02-17"},
            {"name": "The last one"},
        ]

        ids = []

        for task in test_tasks:
            # create task
            response = client.post("/tasks", json=task)
            ids.append(response.json().get("id"))

        # get all tasks
        response = client.get("/tasks")
        data = response.json()
        for row in data:
            database_id = row["id"]
            id = ids.index(database_id)
            assert row["name"] == test_tasks[id].get("name")
            assert row["finished"] == False
            assert row.get("deadline", None) == test_tasks[id].get("deadline", None)
