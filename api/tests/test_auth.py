import time

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from api.core.profiles import FakeProfileStore, get_profile_store
from api.index import app


@pytest.fixture(scope="module")
def rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

@pytest.fixture
def test_app(rsa_keys):
    _, public_pem = rsa_keys
    
    app.state.jwt_key = public_pem
    
    # Fake profile store setup
    profiles = {
        "user_member": "member",
        "user_admin": "admin",
        "user_fake_admin_meta": "member" # user_metadata role=admin but profile role=member
    }
    app.dependency_overrides[get_profile_store] = lambda: FakeProfileStore(profiles)
    
    yield app
    
    # Teardown
    app.dependency_overrides.clear()
    delattr(app.state, "jwt_key")

@pytest.fixture
def client(test_app):
    return TestClient(test_app)

def mint_token(
    private_pem,
    sub: str,
    exp_delta: int = 3600,
    aud: str = "authenticated",
    user_metadata: dict = None,
):
    payload = {
        "sub": sub,
        "aud": aud,
        "iss": "http://testserver/auth/v1",
        "exp": int(time.time()) + exp_delta,
        "email": f"{sub}@example.com"
    }
    if user_metadata:
        payload["user_metadata"] = user_metadata
        
    return jwt.encode(payload, private_pem, algorithm="RS256")



def test_missing_header(client):
    response = client.get("/api/me")
    assert response.status_code == 401

def test_malformed_header(client):
    response = client.get("/api/me", headers={"Authorization": "NotBearer token"})
    assert response.status_code == 401

def test_garbage_token(client):
    response = client.get("/api/me", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401

def test_expired_token(client, rsa_keys):
    private_pem, _ = rsa_keys
    token = mint_token(private_pem, sub="user_member", exp_delta=-3600)
    response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_wrong_audience(client, rsa_keys):
    private_pem, _ = rsa_keys
    token = mint_token(private_pem, sub="user_member", aud="wrong_audience")
    response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_wrong_signature(client):
    # Mint with a new private key
    wrong_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = wrong_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    token = mint_token(private_pem, sub="user_member")
    response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_valid_member_me(client, rsa_keys):
    private_pem, _ = rsa_keys
    token = mint_token(private_pem, sub="user_member")
    response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["role"] == "member"

def test_valid_member_admin_ping(client, rsa_keys):
    private_pem, _ = rsa_keys
    token = mint_token(private_pem, sub="user_member")
    response = client.get("/api/admin/ping", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_valid_admin_admin_ping(client, rsa_keys):
    private_pem, _ = rsa_keys
    token = mint_token(private_pem, sub="user_admin")
    response = client.get("/api/admin/ping", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["role"] == "admin"

def test_no_profile_row(client, rsa_keys):
    private_pem, _ = rsa_keys
    token = mint_token(private_pem, sub="user_not_exist")
    response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_member_with_admin_metadata(client, rsa_keys):
    private_pem, _ = rsa_keys
    token = mint_token(private_pem, sub="user_fake_admin_meta", user_metadata={"role": "admin"})
    response = client.get("/api/admin/ping", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
