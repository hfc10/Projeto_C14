import pytest
from app import app
import models


@pytest.fixture
def client():
    app.config["TESTING"] = True
    models.usuarios.clear()
    with app.test_client() as client:
        yield client


def test_registro_sucesso(client):
    res = client.post(
        "/register", json={"nome_usuario": "user1", "senha": "123"})
    assert res.status_code == 201


def test_registro_dados_faltantes(client):
    res = client.post("/register", json={})
    assert res.status_code == 400


def test_registro_usuario_existente(client):
    client.post("/register", json={"nome_usuario": "user1", "senha": "123"})
    res = client.post(
        "/register", json={"nome_usuario": "user1", "senha": "123"})
    assert res.status_code == 400


def test_login_sucesso(client):
    client.post("/register", json={"nome_usuario": "user1", "senha": "123"})
    res = client.post("/login", json={"nome_usuario": "user1", "senha": "123"})
    assert res.status_code == 200


def test_login_falha(client):
    res = client.post("/login", json={"nome_usuario": "x", "senha": "y"})
    assert res.status_code == 401


def test_get_usuarios(client):
    client.post("/register", json={"nome_usuario": "user1", "senha": "123"})
    res = client.get("/usuarios")
    assert res.status_code == 200
    assert len(res.get_json()) == 1
