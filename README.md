# Prova de Seleção de Estágio - FastAPI, Pydantic e SQLAlchemy

Este projeto é uma API desenvolvida com **Python** utilizando **FastAPI**, **Pydantic** e **SQLAlchemy** para cadastrar empresas e gerenciar suas obrigações acessórias.

## Requisitos do Projeto

- Criar uma API para gerenciar **empresas** e **obrigações acessórias**.
- Utilizar **FastAPI** para desenvolvimento.
- Modelagem de dados com **SQLAlchemy** e **Pydantic**.
- Banco de dados **PostgreSQL**.
- Armazenar credenciais no arquivo **.env**.
- Criar **testes unitários** para os endpoints.
- Documentação automática com **Swagger UI** (/docs).

## Tecnologias Utilizadas

- **Linguagem:** Python 3.9+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de Dados:** PostgreSQL
- **Validação de Dados:** Pydantic
- **Testes:** Pytest
- **Gerenciamento de Dependências:** pip

## Configuração do Ambiente

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```
2. Crie um ambiente virtual e instale as dependências:
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configure o banco de dados PostgreSQL:
   - Crie um banco de dados chamado `minha_empresa_db`.
   - Configure suas credenciais no arquivo `.env`:
     ```ini
     DATABASE_URL=postgresql://usuario:senha@localhost:5432/minha_empresa_db
     ```
4. Execute a migração do banco:
   ```sh
   python main.py  # Isso irá criar as tabelas no banco
   ```

## Executando a API

1. Inicie o servidor FastAPI:
   ```sh
   uvicorn main:app --reload
   ```
2. Acesse a documentação interativa em:
   - [Swagger UI](http://127.0.0.1:8000/docs)
   - [Redoc](http://127.0.0.1:8000/redoc)

## Endpoints da API

### Empresas

- **Criar empresa**: `POST /empresas/`
- **Obter empresa**: `GET /empresas/{empresa_id}`

### Obrigações Acessórias

- **Criar obrigação**: `POST /obrigacoes/`
- **Obter obrigação**: `GET /obrigacoes/{obrigacao_id}`

## Executando os Testes

Para rodar os testes unitários, execute:

```sh
pytest -v
```

Isso irá rodar os testes de criação e obtenção de empresas.

---

Caso tenha dúvidas ou queira contribuir, fique à vontade para abrir uma issue ou pull request. 🚀

