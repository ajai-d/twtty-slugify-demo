from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_slugify_endpoint_ok():
    """AC-5: GET /slugify?text=Hello, World! -> 200 {'slug':'hello-world'}."""
    r = client.get("/slugify", params={"text": "Hello, World!"})
    assert r.status_code == 200
    assert r.json() == {"slug": "hello-world"}


def test_slugify_endpoint_missing_text():
    """AC-6: GET /slugify with no text -> 422."""
    r = client.get("/slugify")
    assert r.status_code == 422


def test_healthz():
    """AC-7: GET /healthz -> 200 {'status':'ok'}."""
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
