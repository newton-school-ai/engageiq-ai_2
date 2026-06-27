from src.utils.auth import create_access_token, verify_token


def test_access_token():
    token = create_access_token(
        {
            "sub": "1",
        }
    )

    payload = verify_token(token)

    assert payload["sub"] == "1"
