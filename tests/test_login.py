from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_success():
    response = client.post(
        "/login",
        data={
            "email": "admin@college.com",
            "password": "admin123",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True