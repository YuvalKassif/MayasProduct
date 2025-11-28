import os
from fastapi.testclient import TestClient
from app.main import app


def _client():
    return TestClient(app)


def _register_and_login(client: TestClient, email: str, password: str):
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 409)
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200


def test_items_crud_guarded():
    if not os.getenv("RUN_DB_TESTS"):
        return
    client = _client()
    _register_and_login(client, "items1@example.com", "Passw0rd!!")

    # Create
    payload = {
        "title": "Blue Jeans",
        "description": "Slim fit",
        "category": "bottoms",
        "brand": "Levi's",
        "size": "M",
        "condition": "good",
        "price_cents": 2500,
        "currency": "USD",
        "location_city": "NYC",
        "location_country": "USA",
    }
    r = client.post("/items", json=payload)
    assert r.status_code == 201
    item = r.json()
    item_id = item["id"]

    # Get
    r = client.get(f"/items/{item_id}")
    assert r.status_code == 200

    # List
    r = client.get("/items?limit=10&offset=0")
    assert r.status_code == 200
    assert "items" in r.json()

    # Update
    r = client.patch(f"/items/{item_id}", json={"price_cents": 2600})
    assert r.status_code == 200
    assert r.json()["price_cents"] == 2600

    # Delete
    r = client.delete(f"/items/{item_id}")
    assert r.status_code == 204

