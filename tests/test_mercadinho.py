import pytest
from mercadinho import Mercadinho

@pytest.fixture
def mercado():
    return Mercadinho()

# --- FLUXO NORMAL (10 Testes) --- 

def test_01_adicionar_item_valido(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("arroz", 2)
    assert sucesso is True
    assert len(mercado.carrinho) == 1

def test_02_reducao_estoque_apos_adicao(mercado):
    estoque_inicial = mercado.estoque["feijao"]["quantidade"]
    mercado.adicionar_ao_carrinho("feijao", 5)
    assert mercado.estoque["feijao"]["quantidade"] == estoque_inicial - 5

def test_03_calcular_total_sem_desconto(mercado):
    mercado.adicionar_ao_carrinho("arroz", 2) # 10.0
    mercado.adicionar_ao_carrinho("leite", 1) # 4.5
    assert mercado.calcular_total() == 14.5

def test_04_aplicar_cupom_valido(mercado):
    mercado.adicionar_ao_carrinho("cafe", 1) # 12.0
    mercado.aplicar_cupom("DEZOFF")
    assert mercado.calcular_total() == 10.8

def test_05_aplicar_cupom_inatel(mercado):
    mercado.adicionar_ao_carrinho("oleo", 2) # 15.0
    mercado.aplicar_cupom("INATEL50")
    assert mercado.calcular_total() == 7.5

def test_06_limpar_carrinho_e_devolver_estoque(mercado):
    mercado.adicionar_ao_carrinho("acucar", 5)
    mercado.limpar_carrinho()
    assert mercado.estoque["acucar"]["quantidade"] == 25
    assert len(mercado.carrinho) == 0

def test_07_adicionar_multiplos_itens_diferentes(mercado):
    mercado.adicionar_ao_carrinho("arroz", 1)
    mercado.adicionar_ao_carrinho("feijao", 1)
    assert len(mercado.carrinho) == 2

def test_08_verificar_dados_do_item_no_carrinho(mercado):
    mercado.adicionar_ao_carrinho("cafe", 1)
    item = mercado.carrinho[0]
    assert item["produto"] == "cafe"
    assert item["preco"] == 12.0

def test_09_total_zero_carrinho_vazio(mercado):
    assert mercado.calcular_total() == 0.0

def test_10_finalizar_venda_sucesso(mercado):
    mercado.adicionar_ao_carrinho("arroz", 1)
    sucesso, msg = mercado.finalizar_venda()
    assert sucesso is True
    assert "Venda finalizada" in msg
    assert len(mercado.carrinho) == 0

