import pytest
from fastapi.testclient import TestClient
from app import main
from app import config

main.settings = config.Settings(_env_file="test.env")  # type: ignore


def test_service_running():
    with TestClient(main.app) as client:
        response = client.get(f"/")
        assert response.status_code == 200


def test_get_empty_task_list():
    with TestClient(main.app) as client:
        response = client.get(f"/tasks")
        assert response.status_code == 404


def test_get_nonexistent_task():
    with TestClient(main.app) as client:
        response = client.get(f"/tasks/id/{99}")
        assert response.status_code == 404


def test_finish_nonexistent_task():
    with TestClient(main.app) as client:
        response = client.put(f"/tasks/id/{99}/finish")
        assert response.status_code == 404


def test_summarize_empty_base():
    with TestClient(main.app) as client:
        response = client.get(f"/tasks/summary")
        assert response.status_code == 200
        assert response.json().get("finished") == 0
        assert response.json().get("active") == 0
        assert response.json().get("total") == 0
