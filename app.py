from flask import Flask, request, jsonify
import models

app = Flask(__name__)


@app.route("/")
def home():
    return {"msg": "API de autenticação rodando"}


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    usuario = models.criar_usuario(
        data.get("nome_usuario") if data else None,
        data.get("senha") if data else None
    )

    if usuario is None:
        return {"error": "Dados inválidos"}, 400

    if usuario == "exists":
        return {"error": "Usuário já existe"}, 400

    return {"msg": "Usuário criado"}, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = models.authenticate(
        data.get("nome_usuario") if data else None,
        data.get("senha") if data else None
    )

    if not usuario:
        return {"error": "Credenciais inválidas"}, 401

    return {"msg": "Login realizado"}


@app.route("/usuarios", methods=["GET"])
def usuarios():
    return jsonify(models.get_usuarios())


if __name__ == "__main__":
    app.run(debug=True)
