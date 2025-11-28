import os

from fastapi.testclient import TestClient

from app.main import app


def _client():
    return TestClient(app)


def test_register_login_me_guarded():
    if not os.getenv("RUN_DB_TESTS"):
        return
    client = _client()
    email = "user1@example.com"
    password = "Passw0rd!!"

    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 409)

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == email

    # We pass token explicitly to /auth/me for simplicity in this guard test
    access = r.cookies.get("access_token")
    assert access
    r = client.get("/auth/me", params={"access_token": access})
    assert r.status_code == 200
    assert r.json()["email"] == email
