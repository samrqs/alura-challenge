# Alura Challenge - Classificador de Feedbacks com IA

Este projeto é parte de um desafio da Alura que propõe a construção de uma aplicação para classificação de sentimentos e extração de intenções a partir de feedbacks de usuários. Utiliza Flask como framework web e integra modelos de linguagem (LLM) para análises automatizadas.

## ⚠️ Requisitos

### 1. Python 3.11+ instalado  
### 2. Uma **chave da API da OpenAI** válida  
### 3. Um servidor SMTP (Gmail, Outlook, etc) para envio de e-mails


## 🔧 Tecnologias utilizadas

- Python 3.11+
- Flask
- SQLAlchemy (SQLite)
- LangChain
- Pipenv
- dotenv

## 🚀 Como executar o projeto localmente com Pipenv

1. **Clone o repositório:**

```bash
git clone https://github.com/samrqs/alura-challenge.git
cd alura-challenge
```

2. **Configure as variáveis de ambiente:**

    Crie um arquivo .env com os seguintes valores:


  
```bash
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=

DATABASE_URL=postgresql://username:password@localhost:5432/feedbacks

OPENAI_API_KEY=sua_chave_api

MAIL_SERVER=smtp.seuprovedor.com
MAIL_PORT=587
MAIL_USERNAME=seuemail@exemplo.com
MAIL_PASSWORD=sua_senha
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER=seuemail@exemplo.com
MAIL_DESTINATARIO=destination@email.com
```

3. **Instale o Pipenv (caso ainda não tenha):**
```bash
pip install pipenv
```

4. **Instale as dependências no ambiente virtual:**
```bash
pipenv install
```

5. **Ative o ambiente virtual:**
```bash
pipenv shell
```

6. **Crie o banco de dados e as tabelas:**
```bash
flask db init       # (somente na primeira vez)
flask db migrate -m "Criação inicial"
flask db upgrade
```

Isso criará um banco SQLite com as tabelas feedbacks e classifications.

7. **Rode a aplicação:**
```bash
flask run
```

## 📮 Endpoints da API 

## 🔹 `POST /feedbacks`

### ➤ Envia um feedback para análise

**Corpo da requisição (JSON):**
```json
{
  "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta"
}
```

## 🔹 `GET /report`

### ➤ Lista relatório simples do andamento de todos os feedbacks

## 🔹 `GET /weekly-summary`

### ➤ Relatório da semana dos feedbacks

## 🔹 `GET /test-email`

### ➤  Endpoint de teste de envio de e-mail do relatório semanal

## 📁 Estrutura do Projeto

```arduino
alura-challenge/
├── app/
│   ├── models/
│   ├── routes/
│   └── services/
├── migrations/
├── run.py
├── Pipfile
├── .env.example
└── README.md
``` 

## 📌 Observações

Certifique-se de ter uma chave da OpenAI válida (OPENAI_API_KEY) para que a análise funcione.
Para testes locais, você pode usar ferramentas como Insomnia ou Postman.
O banco de dados padrão é SQLite, mas pode ser alterado em config.py.