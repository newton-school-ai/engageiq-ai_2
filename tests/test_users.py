from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_users_me_without_token():
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_onboarding_without_token():
    response = client.post(
        "/api/users/onboarding",
        json={
            "role": "student",
            "privacy_mode": "local_only",
        },
    )
    assert response.status_code == 401
