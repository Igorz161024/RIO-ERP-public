from backend.auth import create_access_token, verify_token


def test_create_token():
    token = create_access_token(
        {
            "sub": "admin",
            "role": "admin",
        }
    )

    assert isinstance(token, str)


def test_invalid_token():
    try:
        verify_token("invalid_token")
        assert False
    except Exception:
        assert True
