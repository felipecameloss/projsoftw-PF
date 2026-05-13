from fastapi.testclient import TestClient
from app.main import app
from app.auth import get_current_claims

client = TestClient(app)

def admin_claims():
    return {
        "email": "admin@empresa.com",
        "permissions": ["products:read", "products:create", "products:delete"],
    }

def user_claims():
    return {
        "email": "user@empresa.com",
        "permissions": ["products:read"],
    }

def test_user_can_list():
    app.dependency_overrides[get_current_claims] = user_claims
    r = client.get("/products")
    assert r.status_code == 200
    app.dependency_overrides.clear()

def test_user_cannot_create():
    app.dependency_overrides[get_current_claims] = user_claims
    r = client.post("/products", json={
        "codigo": "P1",
        "nome": "Mouse",
        "preco": 99.9,
        "status": "DISPONIVEL"
    })
    assert r.status_code == 403
    app.dependency_overrides.clear()

def test_admin_can_create():
    app.dependency_overrides[get_current_claims] = admin_claims
    r = client.post("/products", json={
        "codigo": "P1",
        "nome": "Mouse",
        "preco": 99.9,
        "status": "DISPONIVEL"
    })
    assert r.status_code == 201
    app.dependency_overrides.clear()