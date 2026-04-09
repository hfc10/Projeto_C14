# 🛒 Mercadinho — Pipeline CI/CD com Testes Automatizados

> Projeto desenvolvido para a disciplina **C14 – Engenharia de Software**  
> Professor: Christopher Lima

---

## 📋 Sobre o Projeto

Sistema web de um mercadinho virtual desenvolvido com **Flask**, que permite adicionar produtos ao carrinho, aplicar cupons de desconto e finalizar compras. O projeto conta com um pipeline completo de **CI/CD via GitHub Actions**, integrando testes automatizados, build, deploy e notificação por e-mail.

---

## 🏗️ Estrutura do Projeto

```
Projeto_C14/
├── .github/
│   └── workflows/
│       └── ci.yml            # Pipeline CI/CD
├── tests/
│   └── test_mercadinho.py    # 32 testes unitários
├── templates/
│   └── index.html            # Interface web
├── app.py                    # Servidor Flask (API)
├── mercadinho.py             # Lógica de negócio
├── send_notification.py      # Script de notificação por e-mail
├── requirements.txt          # Dependências do projeto
├── .gitignore
└── README.md
```

---

## ⚙️ Funcionalidades

- Estoque com produtos pré-cadastrados (arroz, feijão, leite, café, açúcar, óleo)
- Adicionar produtos ao carrinho com validação de quantidade e estoque
- Aplicar cupons de desconto (`DEZOFF`, `VINTEOFF`, `INATEL50`)
- Calcular total com desconto
- Finalizar venda e limpar carrinho
- Limpar carrinho com devolução de estoque
- Interface web via Flask

---

## 🚀 Como Rodar Localmente

### Pré-requisitos

- Python 3.10+
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/Projeto_C14.git
cd Projeto_C14
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode a aplicação

```bash
python app.py
```

Acesse em: `http://localhost:5000`

---

## 🧪 Como Rodar os Testes

```bash
# Rodar todos os testes
python -m pytest

# Rodar com relatório HTML
python -m pytest --html=report.html --self-contained-html

# Rodar com cobertura de código
python -m pytest --cov=. --cov-report=term-missing
```

---

---

## 🔄 Pipeline CI/CD

O pipeline está configurado no arquivo `.github/workflows/ci.yml` e é ativado a cada push ou pull request para a branch `main`.

### Jobs e fluxo:

```
push/PR
   │
   ├──► [test] Executar Testes (pytest + relatório HTML)
   │
   ├──► [lint] Análise de Código — roda em PARALELO com test
   │
   └──► [build] Build do Projeto ──► (depende de: test)
              │
              └──► [deploy] GitHub Release ──► (depende de: build, só na main)
                       │
                       └──► [notify] Notificação por E-mail ──► (sempre, ao final)
```

### Artefatos gerados:
- `relatorio-testes` — Relatório HTML dos testes (pytest-html)
- `build-projeto` — Pacote `.zip` do projeto

### Deploy:
O deploy é realizado automaticamente via **GitHub Releases**, publicando o pacote `.zip` com versionamento incremental (`v1.0.<run_number>`), somente após os testes e build serem bem-sucedidos.

---

## 🔐 Variáveis de Ambiente (GitHub Secrets)

Configure as seguintes secrets no seu repositório (`Settings > Secrets and variables > Actions`):

| Secret           | Descrição                                     |
|-----------------|-----------------------------------------------|
| `EMAIL_USER`    | E-mail remetente (Gmail)                       |
| `EMAIL_PASS`    | Senha de app do Gmail (não a senha normal)     |
| `EMAIL_RECEIVER`| E-mail(s) destinatário(s), separados por vírgula |

---

## 📦 Dependências

| Pacote        | Versão  | Uso                        |
|--------------|---------|----------------------------|
| flask        | 3.0.0   | Framework web              |
| pytest       | 7.4.3   | Framework de testes        |
| pytest-html  | 4.1.1   | Relatório HTML dos testes  |
| pytest-cov   | 3.0.0   | Cobertura de código        |
| requests     | 2.31.0  | Requisições HTTP           |
| gunicorn     | latest  | Servidor de produção       |

---

## 🌐 Deploy em Produção

A aplicação está hospedada no **Render**:  
🔗 [https://projeto-c14.onrender.com](https://projeto-c14.onrender.com)

O Render detecta automaticamente o `requirements.txt` e utiliza o `gunicorn` para servir a aplicação Flask em produção.

---

## 🤖 Uso de IA

Este projeto utilizou ferramentas de IA (Claude - Anthropic) como apoio no desenvolvimento. Os prompts utilizados cobriram: estruturação do pipeline CI/CD, revisão de código e geração do README. Os resultados foram revisados e adaptados pela equipe.

---

## 👥 Integrantes

| Nome | GitHub |
|------|--------|
| Henrique Fonseca | [@hfc10] |
| Marcus Vinicius de Faria| [@MvJuneau21] |
| Luiz Otávio Amante | [@luizotavio-amante] |
| Jhonata De Oliveira  | [@Jhon4Jhonys] |
| João Vítor Araújo | [@JoaoVACD] |

---

## 📄 Licença

Projeto acadêmico — Inatel C14 – Engenharia de Software
