class Mercadinho:
    def __init__(self):
        # Estoque inicial para testes 
        self.estoque = {
            "arroz": {"preco": 5.0, "quantidade": 20},
            "feijao": {"preco": 8.0, "quantidade": 15},
            "leite": {"preco": 4.5, "quantidade": 30},
            "cafe": {"preco": 12.0, "quantidade": 10},
            "acucar": {"preco": 4.0, "quantidade": 25},
            "oleo": {"preco": 7.5, "quantidade": 12}
        }
        self.cupons_validos = {"DEZOFF": 0.10, "VINTEOFF": 0.20, "INATEL50": 0.50}
        self.carrinho = []
        self.desconto = 0.0
        self.vendas_realizadas = []

    def adicionar_ao_carrinho(self, produto, quantidade):
        try:
            quantidade = int(quantidade)
        except (ValueError, TypeError):
            return False, "Quantidade deve ser um número inteiro"

        if quantidade <= 0:
            return False, "Quantidade inválida"

        if produto not in self.estoque:
            return False, "Produto não encontrado"

        if quantidade > 15:
            return False, "Limite de quantidade por produto excedido"

        if self.estoque[produto]["quantidade"] < quantidade:
            return False, "Estoque insuficiente"

        self.carrinho.append({"produto": produto, "quantidade": quantidade, "preco": self.estoque[produto]["preco"]})
        self.estoque[produto]["quantidade"] -= quantidade
        return True, "Adicionado com sucesso"

    def aplicar_cupom(self, codigo):
        if not codigo:
            return False, "Código vazio"
        if codigo in self.cupons_validos:
            self.desconto = self.cupons_validos[codigo]
            return True, "Cupom aplicado"
        return False, "Cupom inválido ou expirado"

    def calcular_total(self):
        subtotal = sum(item["preco"] * item["quantidade"] for item in self.carrinho)
        total = subtotal * (1 - self.desconto)
        return round(total, 2)

    def finalizar_venda(self):
        if not self.carrinho:
            return False, "Carrinho vazio"
    
        total = self.calcular_total()
    # Registra a venda em um histórico (opcional, mas bom para o projeto)
        self.vendas_realizadas.append({"itens": list(self.carrinho), "total": total})
    
    # O PONTO CRUCIAL: Limpar os dados para a próxima compra
        self.carrinho = [] 
        self.desconto = 0.0
        return True, f"Venda finalizada com sucesso! Total: R${total:.2f}"

    def limpar_carrinho(self):
        # Devolve os itens ao estoque ao limpar
        for item in self.carrinho:
            self.estoque[item["produto"]]["quantidade"] += item["quantidade"]
        self.carrinho = []
        return True