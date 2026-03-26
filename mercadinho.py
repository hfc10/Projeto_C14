class Mercadinho:
    def __init__(self):
        # Estoque expandido para permitir mais cenários de teste [cite: 32]
        self.estoque = {
            "arroz": {"preco": 5.0, "quantidade": 20},
            "feijao": {"preco": 8.0, "quantidade": 15},
            "leite": {"preco": 4.5, "quantidade": 30},
            "cafe": {"preco": 12.0, "quantidade": 10},
            "acucar": {"preco": 4.0, "quantidade": 25},
            "oleo": {"preco": 7.5, "quantidade": 12}
        }
        self.cupons_validos = {"DEZOFF": 0.10,
                               "VINTEOFF": 0.20, "INATEL50": 0.50}
        self.carrinho = []
        self.desconto = 0.0

    def adicionar_ao_carrinho(self, produto, quantidade):
        # Validação de tipo para garantir que quantidade seja numérica
        try:
            quantidade = int(quantidade)
        except ValueError:
            return False, "Quantidade deve ser um número inteiro"

        if produto not in self.estoque:
            return False, "Produto não encontrado"

        if quantidade > 15:
            return False, "Limite de quantidade por produto excedido"

        if self.estoque[produto]["quantidade"] < quantidade:
            return False, "Estoque insuficiente"

        if quantidade <= 0:
            return False, "Quantidade inválida"

        self.carrinho.append({"produto": produto, "quantidade": quantidade})
        self.estoque[produto]["quantidade"] -= quantidade
        return True, "Adicionado com sucesso"

    def aplicar_cupom(self, codigo):
        if codigo in self.cupons_validos:
            self.desconto = self.cupons_validos[codigo]
            return True, "Cupom aplicado"
        return False, "Cupom inválido ou expirado"

    def calcular_total(self):
        subtotal = sum(self.estoque[item["produto"]]["preco"]
                       * item["quantidade"] for item in self.carrinho)
        total = subtotal * (1 - self.desconto)
        return round(total, 2)
