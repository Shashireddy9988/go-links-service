import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.repositories.link_repository import InMemoryLinkRepository

@pytest.fixture
def client():
    repo = InMemoryLinkRepository(seed=False)
    app = create_app(repo=repo)
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_fetch_links(client):
    payload = {
        "alias": "design-system",
        "target_url": "https://storybook.js.org",
        "title": "Design System",
        "tags": ["design"]
    }
    create_res = client.post("/api/v1/links", json=payload)
    assert create_res.status_code == 201
    assert create_res.json()["data"]["alias"] == "design-system"

    get_res = client.get("/api/v1/links")
    assert get_res.status_code == 200
    assert len(get_res.json()["data"]) == 1

def test_redirect_302(client):
    payload = {
        "alias": "dashboard",
        "target_url": "https://grafana.com/dashboards",
        "title": "Grafana"
    }
    client.post("/api/v1/links", json=payload)

    response = client.get("/go/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://grafana.com/dashboards"

def test_404_redirect(client):
    response = client.get("/go/missing-link", follow_redirects=False)
    assert response.status_code == 404
