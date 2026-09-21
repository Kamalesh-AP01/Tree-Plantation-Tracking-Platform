from unittest.mock import MagicMock

from app.services.user_service import get_user_by_email


def test_get_user_by_email():
    db = MagicMock()

    test_user = MagicMock()
    test_user.email = "testuser@gmail.com"

    db.query.return_value.filter.return_value.first.return_value = test_user

    result = get_user_by_email(
        db,
        "testuser@gmail.com"
    )

    assert result is test_user
    assert result.email == "testuser@gmail.com"