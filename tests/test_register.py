from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    email = "pytest_user_001@gmail.com"

    response = client.post(
        "/register",
        data={
            "name": "Pytest User",
            "email": email,
            "password": "test123",
        },
    )

    assert response.status_code in [200, 400]

    if response.status_code == 200:
        assert response.json()["success"] is True