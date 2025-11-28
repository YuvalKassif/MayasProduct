import os
from fastapi.testclient import TestClient
from app.main import app


def test_db_health_guarded():
    # Only run if an integration DB is expected to be available
    if not os.getenv("RUN_DB_TESTS"):
        return
    client = TestClient(app)
    r = client.get("/health/db")
    assert r.status_code == 200
    assert r.json().get("database") == "ok"

