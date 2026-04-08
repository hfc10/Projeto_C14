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

# --- FLUXO DE EXTENSÃO / ERRO (10 testes) ---

def test_11_produto_nao_encontrado(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("banana", 2)
    assert sucesso is False
    assert msg == "Produto não encontrado"


def test_12_quantidade_nao_numerica(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("arroz", "abc")
    assert sucesso is False
    assert msg == "Quantidade deve ser um número inteiro"


def test_13_quantidade_zero(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("arroz", 0)
    assert sucesso is False
    assert msg == "Quantidade inválida"


def test_14_quantidade_negativa(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("arroz", -1)
    assert sucesso is False
    assert msg == "Quantidade inválida"


def test_15_estoque_insuficiente(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("cafe", 12)
    assert sucesso is False
    assert msg == "Estoque insuficiente"


def test_16_limite_quantidade_excedido(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("arroz", 16)
    assert sucesso is False
    assert msg == "Limite de quantidade por produto excedido"


def test_17_cupom_invalido(mercado):
    sucesso, msg = mercado.aplicar_cupom("ERRADO")
    assert sucesso is False
    assert msg == "Cupom inválido ou expirado"


def test_18_cupom_vazio(mercado):
    sucesso, msg = mercado.aplicar_cupom("")
    assert sucesso is False
    assert msg == "Código vazio"


def test_19_nao_altera_estoque_em_operacao_invalida(mercado):
    estoque_inicial = mercado.estoque["arroz"]["quantidade"]
    sucesso, msg = mercado.adicionar_ao_carrinho("arroz", 0)

    assert sucesso is False
    assert msg == "Quantidade inválida"
    assert mercado.estoque["arroz"]["quantidade"] == estoque_inicial


def test_20_carrinho_permanece_vazio_apos_falha(mercado):
    sucesso, msg = mercado.adicionar_ao_carrinho("produto_inexistente", 3)

    assert sucesso is False
    assert msg == "Produto não encontrado"
    assert len(mercado.carrinho) == 0



    # Fluxo Histórico/Persistência: 21-30

def test_21_finalizar_venda_registra_historico(mercado):
   
    mercado.adicionar_ao_carrinho("arroz", 2)   # 10.0
    mercado.adicionar_ao_carrinho("leite", 1)   # 4.5
    mercado.finalizar_venda()

    assert len(mercado.vendas_realizadas) == 1
    venda = mercado.vendas_realizadas[0]
    assert venda["total"] == 14.5
    assert len(venda["itens"]) == 2


def test_22_carrinho_limpo_apos_finalizar_venda(mercado):
    """
    Após finalizar a venda, o carrinho deve ser zerado e o desconto
    resetado, permitindo uma nova compra sem resíduos do estado anterior.
    """
    mercado.adicionar_ao_carrinho("cafe", 1)
    mercado.aplicar_cupom("DEZOFF")     # 10% de desconto
    mercado.finalizar_venda()

    assert len(mercado.carrinho) == 0
    assert mercado.desconto == 0.0
    assert mercado.calcular_total() == 0.0


def test_23_cupom_vinteoff_desconto_vinte_porcento(mercado):
    """
    Valida o cupom VINTEOFF aplicando 20% de desconto sobre o subtotal.
    Verifica o cálculo aritmético e o arredondamento para 2 casas decimais.
    """
    mercado.adicionar_ao_carrinho("oleo", 2)    # 7.5 * 2 = 15.0
    sucesso, msg = mercado.aplicar_cupom("VINTEOFF")

    assert sucesso is True
    assert mercado.calcular_total() == 12.0     # 15.0 * 0.80


def test_24_multiplas_vendas_acumulam_historico(mercado):
    """
    Simula duas compras completas consecutivas e verifica que ambas
    ficam registradas no histórico de vendas_realizadas com totais corretos.
    """
    # Primeira venda
    mercado.adicionar_ao_carrinho("acucar", 1)  # 4.0
    mercado.finalizar_venda()

    # Segunda venda
    mercado.adicionar_ao_carrinho("leite", 2)   # 9.0
    mercado.finalizar_venda()

    assert len(mercado.vendas_realizadas) == 2
    assert mercado.vendas_realizadas[0]["total"] == 4.0
    assert mercado.vendas_realizadas[1]["total"] == 9.0


def test_25_estoque_nao_alterado_apos_limpar_carrinho(mercado):
   
    qtd_inicial_arroz = mercado.estoque["arroz"]["quantidade"]   # 20
    qtd_inicial_feijao = mercado.estoque["feijao"]["quantidade"] # 15

    mercado.adicionar_ao_carrinho("arroz", 3)
    mercado.adicionar_ao_carrinho("feijao", 4)
    mercado.limpar_carrinho()

    assert mercado.estoque["arroz"]["quantidade"] == qtd_inicial_arroz
    assert mercado.estoque["feijao"]["quantidade"] == qtd_inicial_feijao

def test_26_finalizar_venda_carrinho_vazio(mercado):
    
    sucesso, msg = mercado.finalizar_venda()

    assert sucesso is False
    assert msg == "Carrinho vazio"
    assert len(mercado.vendas_realizadas) == 0


def test_27_cupom_case_sensitive_nao_aceita_minusculo(mercado):
   
    mercado.adicionar_ao_carrinho("arroz", 1)
    sucesso, msg = mercado.aplicar_cupom("dezoff")

    assert sucesso is False
    assert msg == "Cupom inválido ou expirado"


def test_28_estoque_zerado_apos_compra_maxima(mercado):
   
    estoque_cafe = mercado.estoque["cafe"]["quantidade"]  # 10

    # Compra o máximo permitido por transação (até o limite de 15,
    # mas o estoque do café é 10)
    mercado.adicionar_ao_carrinho("cafe", 10)
    mercado.finalizar_venda()

    # Nova tentativa com estoque zerado
    sucesso, msg = mercado.adicionar_ao_carrinho("cafe", 1)

    assert sucesso is False
    assert msg == "Estoque insuficiente"
    assert mercado.estoque["cafe"]["quantidade"] == 0


def test_29_desconto_nao_persiste_entre_compras(mercado):
   
    # Primeira compra com desconto
    mercado.adicionar_ao_carrinho("arroz", 2)   # 10.0
    mercado.aplicar_cupom("DEZOFF")             # 10% → 9.0
    mercado.finalizar_venda()

    # Segunda compra — NÃO deve ter desconto
    mercado.adicionar_ao_carrinho("arroz", 2)   # 10.0

    assert mercado.calcular_total() == 10.0     # sem desconto residual
