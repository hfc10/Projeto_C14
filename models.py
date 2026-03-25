usuarios = []


def criar_usuario(nome_usuario, senha):
    if not nome_usuario or not senha:
        return None

    if any(u["nome_usuario"] == nome_usuario for u in usuarios):
        return "exists"

    usuario = {
        "id": len(usuarios) + 1,
        "nome_usuario": nome_usuario,
        "senha": senha
    }

    usuarios.append(usuario)
    return usuario


def authenticate(nome_usuario, senha):
    for usuario in usuarios:
        if usuario["nome_usuario"] == nome_usuario and usuario["senha"] == senha:
            return usuario
    return None


def get_usuarios():
    return usuarios
