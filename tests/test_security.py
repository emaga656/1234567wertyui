from app.core.security import hash_password, verify_password, create_access_token, decode_token

def test_password_hashing():
    hashed = hash_password("StrongPass123")
    assert hashed != "StrongPass123"
    assert verify_password("StrongPass123", hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_roundtrip():
    token = create_access_token("42")
    assert decode_token(token)["sub"] == "42"
