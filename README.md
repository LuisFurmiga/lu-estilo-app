# Lu Estilo APP - API

API RESTful desenvolvida com **FastAPI** para gerenciamento de **clientes**, **produtos** e **pedidos** com autenticação via JWT, documentação Swagger e deploy com Docker.

---

## 🔧 Funcionalidades

### 🧑 Clientes
- `GET /clients` — Listar clientes (com paginação e filtros)
- `POST /clients` — Criar novo cliente (validação de CPF e email)
- `GET /clients/{id}` — Obter cliente por ID
- `PUT /clients/{id}` — Atualizar cliente
- `DELETE /clients/{id}` — Excluir cliente

### 📦 Produtos
- `GET /products` — Listar produtos (filtros por seção, disponibilidade, preço)
- `POST /products` — Criar produto com descrição, valor, seção, validade, imagem, etc.
- `GET /products/{id}` — Detalhar produto
- `PUT /products/{id}` — Atualizar produto
- `DELETE /products/{id}` — Excluir produto

### 📋 Pedidos
- `GET /orders` — Listar pedidos (filtros por período, status, cliente, id e seção)
- `POST /orders` — Criar pedido (com validação de estoque)
- `GET /orders/{id}` — Obter pedido
- `PUT /orders/{id}` — Atualizar status
- `DELETE /orders/{id}` — Excluir pedido

### 🔐 Autenticação
- `POST /auth/register` — Registrar novo usuário
- `POST /auth/login` — Autenticar e gerar token
- `POST /auth/refresh-token` — Renovar token

---

## 🛡️ Segurança
- Autenticação via JWT
- Proteção de rotas com `Depends(get_current_user)`
- Senhas armazenadas com hashing seguro
- Middleware de tratamento de erros e integração com **Sentry**

---

## ⚙️ Instalação com Docker

1. Renomeie `.env.example` para `.env` e configure as variáveis
2. Suba os containers:

```bash
docker-compose up --build
```

3. Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Executando os Testes

```bash
pytest -s
```

- Banco de testes isolado
- Cobertura: autenticação, clientes, produtos, pedidos

---

## 🐳 Estrutura do Docker

- **web**: container FastAPI
- **db**: PostgreSQL 14 com volume persistente
- Scripts automáticos de criação do banco

---

## 🧠 Tecnologias

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- Pytest
- Docker + docker-compose
- Sentry (monitoramento)
- Pydantic v2

---

## ✨ Swagger

Documentação interativa disponível em:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados
- Porta 8000 disponível no seu computador

### Passos

1. Clone o repositório:

```bash
git clone https://github.com/LuisFurmiga/lu-estilo-app.git
cd lu-estilo-app
```

2. Crie o `.env` e ajuste conforme necessário:

```bash
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/luestilo
SECRET_KEY="Furmiga!QualAChaveSecreta?"
ALGORITHM="HS256"
EXPIRE_MINUTES=30
SENTRY_DSN="LinkDoSentryAqui"
```

3. Suba a aplicação com Docker:

```bash
docker-compose up --build
```

4. Acesse no navegador:

- Aplicação: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs

### Rodando os testes

```bash
docker-compose exec web pytest -s
```

---

Desenvolvido para o processo seletivo da [INFOG2](http://www.infog2.com.br/)
