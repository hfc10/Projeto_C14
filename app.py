# Adicionado render_template
from flask import Flask, jsonify, request, render_template
from mercadinho import Mercadinho

app = Flask(__name__)
loja = Mercadinho()


@app.route('/')
def home():
    # Removido o jsonify daqui para que a página HTML carregue corretamente
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
            "qtd": quantidade,
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


if __name__ == '__main__':
    app.run(debug=True)
