from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_register_login_and_create_project():
    # register
    r = client.post("/auth/register", json={"email": "ci@example.com", "password": "secret12345"})
    assert r.status_code in (201, 400)  # ok if already exists

    # login
    r = client.post("/auth/login", json={"email": "ci@example.com", "password": "secret12345"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create project
    r = client.post("/projects", json={"name": "CI Demo", "description": "pipeline test"}, headers=headers)
    assert r.status_code in (200, 201)
    pid = r.json()["id"]

    # list tasks (should work even if empty)
    r = client.get(f"/projects/{pid}/tasks", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert "items" in body and "total" in body
