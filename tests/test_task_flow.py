import pytest
from fastapi.testclient import TestClient
from app import main
from app import config

main.settings = config.Settings(_env_file="test.env") # type: ignore

def test_flow():
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

        # finish a task
        id_to_finish = ids[2]
        response = client.put(f"/tasks/id/{id_to_finish}/finish")

        # get summary
        response = client.get("/tasks/summary")
        assert response.status_code == 200
        assert response.json().get("finished") == 1
        assert response.json().get("active") == 3
        assert response.json().get("total") == 4
