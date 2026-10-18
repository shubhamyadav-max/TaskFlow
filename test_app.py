
import pytest
import app as app_module
from app import app, tasks


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    app_module.next_id = 1
    yield
    tasks.clear()
    app_module.next_id = 1


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data


def test_add_task(client):
    response = client.post(
        "/add",
        data={"title": "Complete project", "priority": "High"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Complete project" in response.data


def test_update_task(client):
    client.post(
        "/add",
        data={"title": "Study", "priority": "Medium"}
    )
    client.post("/update/1")
    assert tasks[0]["status"] == "In Progress"


def test_delete_task(client):
    client.post(
        "/add",
        data={"title": "Study", "priority": "Low"}
    )
    client.post("/delete/1")
    assert len(tasks) == 0


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
