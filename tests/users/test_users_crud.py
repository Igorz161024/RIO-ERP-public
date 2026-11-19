from backend.models.user import User


def test_user_model_create():
    user = User(
        username="testuser",
        email="test@test.com",
        password_hash="hash",
        role="user",
    )

    assert user.username == "testuser"


def test_user_email_type():
    user = User(
        email="test@test.com"
    )

    assert isinstance(user.email, str)


def test_user_role_type():
    user = User(
        role="user"
    )

    assert isinstance(user.role, str)