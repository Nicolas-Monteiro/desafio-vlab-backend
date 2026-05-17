# V-Lab Data Lake Gateway API

Uma API robusta e assíncrona construída com **FastAPI** para atuar como Gateway de Ingestão de um Data Lake do setor de transportes. O sistema foi desenhado para receber, validar e centralizar informações de abastecimento de frotas em nível nacional, suportando alta demanda de leitura e escrita.

##  Funcionalidades Entregues

* **Ingestão de Dados Segura:** Validação matemática de CPFs e tipos de dados estritos via Pydantic.
* **Detecção de Anomalias:** Regra de negócio que marca registros como `improper_data = true` se o valor exceder a média histórica.
* **Autenticação:** Rota de ingestão (POST) protegida por **API Key** via cabeçalho HTTP (`X-API-Key`).
* **Consultas de Alta Performance:** Endpoints de leitura paginados, com filtros (tipo e data) e otimizados com cache em **Redis**.
* **Banco de Dados Relacional:** Persistência em **PostgreSQL** com versionamento de esquema utilizando **Alembic**.
* **Testes Automatizados:** Cobertura de rotas e regras de validação (caminhos felizes e tristes) usando **Pytest**.
* **Teste de Estresse Integrado:** Serviço autônomo rodando no Docker que gera dados fictícios realistas (Faker) para bombardeamento da API.
* **Padronização de Código:** Linting e formatação rigorosos garantidos pelo **Ruff** (aderência total à PEP 8).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework Web:** FastAPI
* **Banco de Dados:** PostgreSQL
* **Cache:** Redis
* **ORM & Migrations:** SQLAlchemy + Alembic
* **Infraestrutura:** Docker & Docker Compose
* **Qualidade & Testes:** Pytest, HTTPX, Ruff, Faker

---

## ⚙️ Como Executar o Projeto

O projeto foi totalmente containerizado para garantir que rode em qualquer ambiente sem necessidade de configurações locais complexas.

1. Clone o repositório:
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd desafio-vlab-backend
```

2. Configure as variáveis de ambiente:
Copie o arquivo de exemplo para criar o seu próprio arquivo `.env`. Os valores padrão já vêm configurados com a string de conexão pronta para o ambiente Docker:
```bash
cp .env.example .env
```

3. Suba a infraestrutura completa (API, Postgres, Redis e Serviço de Carga):
```bash
docker-compose up --build -d
```

A API estará disponível em: `http://localhost:8000`

---

## 📚 Documentação da API (Swagger)

O FastAPI gera a documentação interativa automaticamente. Com os containers rodando, acesse:
 **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Autenticação na Rota POST
Para testar a criação de um abastecimento via Swagger:
1. Clique no botão **Authorize** (cadeado) no topo da página.
2. Insira a chave secreta de desenvolvimento: `vlab-token-super-secreto-2026`
3. Execute o teste na rota `POST /api/v1/abastecimentos/`.

---

## 🧪 Como Rodar os Testes Automatizados

O projeto utiliza Pytest para testes de integração e regras de negócio. Para executá-los dentro do ambiente Docker, rode:

```bash
docker-compose exec api pytest
```

---

## 🧹 Padronização de Código (Linting)

O código segue as diretrizes da PEP 8. O **Ruff** foi configurado para verificar erros e formatar a base de código.

Para checar inconsistências:
```bash
docker-compose exec api ruff check
```

Para aplicar a formatação automática:
```bash
docker-compose exec api ruff format
```

---

##  Teste de Estresse (Load Tester)

Para demonstrar a capacidade da API, um serviço chamado `load_tester` é iniciado automaticamente com o Docker Compose. Ele aguarda a API estar 100% online e começa a disparar requisições em massa (gerando CPFs e dados matematicamente válidos) para popular o banco de dados.

Para visualizar o funcionamento do teste em tempo real, acompanhe os logs:
```bash
docker-compose logs -f load_tester
```