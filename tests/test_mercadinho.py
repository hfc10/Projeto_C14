import pytest
from mercadinho import Mercadinho


@pytest.fixture
def loja():
    """Fixture para inicializar a classe Mercadinho antes de cada teste"""
    return Mercadinho()

# --- 1. Fluxo Normal (Cenário de Sucesso) ---


def test_adicionar_produto_sucesso(loja):
    """
    Testa se um produto existente com quantidade válida 
    é adicionado corretamente ao carrinho.
    """
    sucesso, mensagem = loja.adicionar_ao_carrinho("arroz", 2)

    assert sucesso is True
    assert mensagem == "Adicionado com sucesso"
    assert loja.calcular_total() == 10.0  # 2 * 5.0 (preço do arroz)


# --- 2. Fluxo Inoportuno (Cenário de Erro) ---
def test_estoque_insuficiente(loja):
    """
    Testa a tentativa de compra de uma quantidade maior 
    do que a disponível no estoque (Fluxo de Exceção).
    """
    # O estoque inicial de café é 10. Tentaremos comprar 12.
    sucesso, mensagem = loja.adicionar_ao_carrinho("cafe", 12)

    assert sucesso is False
    assert mensagem == "Estoque insuficiente"
    assert loja.calcular_total() == 0.0  # O carrinho deve continuar vazio
