**viva-control-backend** é o servidor backend do Viva Control — sistema de gestão web para distribuidores e vendedores parceiros da Viva Professional.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

### 📖 Glossário de Tecnologias

| Tecnologia       | Descrição                                                                                                                                                             |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flask            | Microframework web em Python. Provê o servidor HTTP, roteamento e o ciclo de vida da aplicação.                                                                       |
| Flask-RESTX      | Extensão do Flask para construção de APIs REST. Adiciona organização por Namespaces, validação de payload e geração automática de documentação via Swagger UI em `/`. |
| Swagger UI       | Interface gráfica para documentação interativa e teste da API REST. Gerada automaticamente pelo Flask-RESTX a partir dos Namespaces e Resources, disponível em `/`.   |
| Flask-SQLAlchemy | Integração entre Flask e SQLAlchemy. Gerencia a sessão do banco de dados e o ciclo de vida da conexão dentro do contexto da aplicação.                                |
| SQLAlchemy       | ORM e toolkit SQL em Python. Mapeia classes Python a tabelas relacionais e gerencia transações.                                                                       |
| Flask-Migrate    | Controle de versão do esquema do banco de dados via Alembic. Gera e aplica scripts de migração a partir das alterações nos modelos.                                   |
| Flask-CORS       | Gerenciamento de Cross-Origin Resource Sharing. Controla quais origens têm permissão para consumir a API.                                                             |
| SQLite           | Banco de dados relacional embutido, sem necessidade de servidor. Utilizado no ambiente de desenvolvimento pelo custo zero de infraestrutura.                          |
| PostgreSQL       | Banco de dados relacional com suporte completo a transações ACID e controle de concorrência por linha. Escolha para o ambiente de produção.                           |

## 🛠️ Instalação e Execução

Desenvolvido em **Python 3.12**, recomenda-se o uso dessa versão para garantir compatibilidade. A seguir, os passos para configuração e execução a partir do diretório raiz:

### 1️⃣ Criar e Ativar o Ambiente Virtual

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Definir Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

- `DATABASE_URI` — URI de conexão com o banco de dados (ex.: `sqlite:///database.sqlite3` ou `postgresql://user:password@host/db`).
- `ALLOWED_HOSTS` — Origens permitidas pelo CORS, separadas por espaço (ex.: `http://localhost:5173`).

### 4️⃣ Aplicar Migrações

```bash
flask db upgrade
```

### 5️⃣ Iniciar o Servidor de Desenvolvimento

```bash
flask run
```

A documentação Swagger da API estará disponível em `http://localhost:5000/`.

## 📐 Princípios do Projeto

O backend adota os princípios da Clean Architecture como guia de organização, com separação explícita entre as camadas e dependências fluindo de fora para dentro: a camada de APIs depende de serviços; serviços dependem de modelos; modelos não dependem de nenhuma camada superior.

<p align="center">
  <img src="./static/img/the-clean-architecture.png" alt="The Clean Architecture" width="500" />
  <img src="./static/img/the-clean-architecture-cone.png" alt="The Clean Architecture Cone" width="500" />
</p>

| Camada               | Diretório(s)                       |
| -------------------- | ---------------------------------- |
| Entities             | `models/`                          |
| Use Cases            | `services/`                        |
| Interface Adapters   | `schemas/`, `apis/`                |
| Frameworks & Drivers | `config/`, `exceptions/`, `utils/` |

A implementação é majoritariamente procedural com elementos de orientação a objetos: os serviços são funções puras que operam sobre modelos ORM, enquanto os modelos utilizam mixins para compartilhar comportamento comum — persistência, timestamps e chave primária — sem herança profunda.

O controle de acesso (RBAC) com três perfis — `ADMIN`, `DISTRIBUTOR` e `SELLER` — é aplicado e validado integralmente no backend. Registros não são excluídos fisicamente: a remoção é feita por inativação (`is_active = FALSE`), preservando o histórico e os vínculos com pedidos e cobranças.

## 🗂️ Estruturação

```
viva-control-backend/
├── app/
│   ├── models/
│   │   ├── contract/
│   │   └── mixin/
│   ├── services/
│   │   └── contract/
│   ├── schemas/
│   │   ├── contract/
│   │   └── mixin/
│   ├── apis/
│   ├── exceptions/
│   │   └── base/
│   ├── utils/
│   └── config/
└── migrations/
    └── versions/
```

### 📁 `app/`

Código-fonte principal.

#### 📁 `models/`

Camada de **persistência** — modelos SQLAlchemy. O subdiretório `contract/` define classes abstratas e Protocols que estabelecem contratos de comportamento obrigatórios. O subdiretório `mixin/` expõe mixins reutilizáveis: chave primária autoincrementada, métodos `save` e `delete`, e colunas de auditoria `created_at` e `updated_at`.

#### 📁 `services/`

Camada de **lógica de negócio** — funções procedurais que operam sobre os modelos e orquestram as regras de cada domínio. O subdiretório `contract/` contém contratos abstratos para serviços.

#### 📁 `schemas/`

Contratos de serialização e validação da API — modelos Flask-RESTX (`api.model()`). O subdiretório `contract/` define contratos abstratos; o subdiretório `mixin/` expõe campos reutilizáveis, como `timestamp_fields`, para serem espalhados em qualquer schema.

#### 📁 `apis/`

Camada de **apresentação** — Namespaces e Resources do Flask-RESTX. Cada arquivo define um Namespace com as rotas e os decorators de validação, documentação e resposta. Não contém lógica de negócio: delega toda operação ao serviço correspondente.

#### 📁 `exceptions/`

Hierarquia de exceções HTTP da aplicação. A classe raiz `ApiException`, no subdiretório `base/`, herda de `HTTPException` e expõe o classmethod `get_response()` para compor tuplas de resposta nos decorators `@ns.response`. As exceções concretas combinam `ApiException` com as exceções HTTP do Werkzeug via herança múltipla.

#### 📁 `utils/`

Utilitários transversais sem vínculo com um domínio específico. Concentra funções auxiliares para declaração de colunas e relacionamentos SQLAlchemy, além de constantes de padrões de validação reutilizáveis nas schemas.

#### 📁 `config/`

Configuração e inicialização da aplicação:

- 📄 `paths.py` — Constantes de caminhos do sistema de arquivos (`ROOT_DIR`, `ENV_FILE`, `DATABASE_FILE`).
- 📄 `environs.py` — Variáveis de ambiente lidas via `os.environ`, com valores padrão para desenvolvimento.
- 📄 `setup.py` — Funções procedurais `setup_environs` e `setup_extensions`, responsáveis por aplicar parâmetros ao `app` e inicializar as extensões Flask.

### 📁 `migrations/`

Gerenciado pelo Flask-Migrate, armazena os scripts de migração do banco no diretório 📁 `versions/`.

## 📚 Referências

- Clean Architecture — Uma abordagem baseada em princípios. Medium, disponível em: [medium.com/@gabrielfernandeslemos/clean-architecture-uma-abordagem-baseada-em-princípios-bf9866da1f9c](https://medium.com/@gabrielfernandeslemos/clean-architecture-uma-abordagem-baseada-em-princípios-bf9866da1f9c).
- O que exatamente é Clean Architecture (Arquitetura Limpa)? Como e onde usar? Stack Overflow em Português, disponível em: [pt.stackoverflow.com/questions/441073](https://pt.stackoverflow.com/questions/441073/o-que-exatamente-%C3%A9-clean-architecture-arquitetura-limpa-como-e-onde-usar).
- Sweet Server. GitHub, disponível em: [github.com/pedrovitorsilva/sweet-server](https://github.com/pedrovitorsilva/sweet-server).
