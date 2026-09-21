from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_admin_login_has_admin_role():
    response = client.post(
        "/login",
        data={
            "email": "admin@college.com",
            "password": "admin123",
        },
    )

    assert response.status_code == 200
    assert response.json()["role_id"] == 1


def test_user_login_has_user_role():
    response = client.post(
        "/login",
        data={
            "email": "testuser@gmail.com",
            "password": "test123",
        },
    )

    assert response.status_code == 200
    assert response.json()["role_id"] == 2