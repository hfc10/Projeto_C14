from flask import Flask, jsonify, request, render_template
from mercadinho import Mercadinho

app = Flask(__name__)
loja = Mercadinho()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    produto = request.args.get('produto')
    quantidade = request.args.get('quantidade')

    if not produto or not quantidade:
        return jsonify({"erro": "Informe produto e quantidade na URL"}), 400

    sucesso, mensagem = loja.adicionar_ao_carrinho(produto, quantidade)
    if sucesso:
        return jsonify({
            "mensagem": mensagem,
            "item": produto,
            "qtd": int(quantidade),
            "total_carrinho": loja.calcular_total()
        }), 200
    return jsonify({"erro": mensagem}), 400

@app.route('/cupom')
def aplicar_cupom():
    codigo = request.args.get('codigo', '')
    sucesso, mensagem = loja.aplicar_cupom(codigo)
    if sucesso:
        return jsonify({"mensagem": mensagem, "novo_total": loja.calcular_total()}), 200
    return jsonify({"erro": mensagem}), 400

# NOVA ROTA: Necessária para o Teste 10 e para o critério de Deploy funcional 
@app.route('/finalizar')
def finalizar():
    # Chama o método que criamos no mercadinho.py
    sucesso, mensagem = loja.finalizar_venda()
    if sucesso:
        # Se sucesso, o carrinho já foi limpo dentro do método finalizar_venda()
        return jsonify({"mensagem": mensagem, "status": "sucesso"}), 200
    return jsonify({"erro": mensagem}), 400

if __name__ == '__main__':
    app.run(debug=True)