**viva-control-backend** é o servidor backend do Viva Control — sistema de gestão web para distribuidores parceiros da Viva Professional.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

### 📖 Glossário de Tecnologias

| Tecnologia         | Descrição                                                                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flask              | Microframework web em Python. Provê o servidor HTTP, roteamento e o ciclo de vida da aplicação.                                                                     |
| Flask-RESTX        | Extensão do Flask para construção de APIs REST. Adiciona organização por namespaces, validação de payload e geração automática de documentação via Swagger UI.      |
| Swagger UI         | Interface gráfica para documentação interativa e teste da API REST. Gerada automaticamente pelo Flask-RESTX a partir dos namespaces e resources, disponível em `/`. |
| Flask-SQLAlchemy   | Integração entre Flask e SQLAlchemy. Gerencia a sessão do banco de dados e o ciclo de vida da conexão dentro do contexto da aplicação.                              |
| SQLAlchemy         | ORM e toolkit SQL em Python. Mapeia classes Python a tabelas relacionais e gerencia transações.                                                                     |
| Flask-Migrate      | Controle de versão do esquema do banco de dados via Alembic. Gera e aplica scripts de migração a partir das alterações nos modelos.                                 |
| Flask-JWT-Extended | Autenticação stateless via JSON Web Token. Gerencia emissão, validação e proteção de rotas com `@jwt_required()`, além de claims adicionais no payload do token.    |
| Flask-CORS         | Gerenciamento de Cross-Origin Resource Sharing. Controla quais origens têm permissão para consumir a API.                                                           |
| SQLite             | Banco de dados relacional embutido, sem necessidade de servidor. Utilizado no ambiente de desenvolvimento pelo custo zero de infraestrutura.                        |
| PostgreSQL         | Banco de dados relacional com suporte completo a transações ACID e controle de concorrência por linha. Escolha para o ambiente de produção.                         |
| pytest             | Framework de testes para Python. Suporta fixtures, parametrização e integração com `unittest.mock` para isolamento da lógica de negócio.                            |

## 🛠️ Instalação e Execução

Desenvolvido em **Python 3.14**, recomenda-se o uso dessa versão para garantir compatibilidade. A seguir, os passos para configuração e execução a partir do diretório raiz:

### 1️⃣ Criar e Ativar o Ambiente Virtual

```bash
# Windows
python -m venv .venv

# Linux / macOS
python3 -m venv .venv
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

Copie o arquivo `.env.example` para `.env` na raiz do projeto e preencha as variáveis:

```bash
cp .env.example .env
```

| Variável                                 | Descrição                                                                                                      |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `ADMIN_EMAIL`                            | E-mail do usuário administrador criado automaticamente na primeira inicialização, se ainda não existir.        |
| `ADMIN_PASSWORD`                         | Senha do usuário administrador criado automaticamente na primeira inicialização, se ainda não existir.         |
| `ALLOWED_HOSTS`                          | Origens permitidas pelo CORS, separadas por espaço (ex.: `http://localhost:5173`). Use `*` em desenvolvimento. |
| `DATABASE_URI`                           | URI de conexão com o banco (ex.: `sqlite:///database.sqlite3` ou `postgresql://user:password@host/db`).        |
| `JWT_SECRET_KEY`                         | Chave secreta para assinar os tokens JWT. Deve ser uma string longa e aleatória em produção.                   |
| `JWT_ACCESS_TOKEN_EXPIRATION_IN_MINUTES` | Duração em minutos do token de acesso JWT. Padrão: `15`.                                                       |
| `JWT_REFRESH_TOKEN_EXPIRATION_IN_DAYS`   | Duração em dias do token de atualização JWT. Padrão: `30`.                                                     |

### 4️⃣ Aplicar Migrações

```bash
flask db upgrade
```

### 5️⃣ Iniciar o Servidor de Desenvolvimento

```bash
flask run
```

A documentação Swagger da API estará disponível em `http://localhost:5000/`.

## 🧪 Cobertura de Testes

A suíte cobre a camada de serviços (`app/services/`) com testes unitários. A lógica de negócio é isolada via `unittest.mock` — dependências externas como banco de dados e servidor HTTP são substituídas por mocks. Para executar, utilize o comando:

```bash
pytest tests/ --verbose
```

## 📐 Princípios do Projeto

O backend adota os princípios da Clean Architecture como guia de organização, com separação explícita entre as camadas e dependências fluindo de fora para dentro: a camada de APIs depende de serviços; serviços dependem de modelos; modelos não dependem de nenhuma camada superior.

<p align="center">
  <img src="./static/img/the-clean-architecture.png" alt="The Clean Architecture" width="500" />
  <img src="./static/img/the-clean-architecture-cone.png" alt="The Clean Architecture Cone" width="500" />
</p>

| Camada               | Diretório(s)                                                                  |
| -------------------- | ----------------------------------------------------------------------------- |
| Entities             | `app/models/`                                                                 |
| Use Cases            | `app/services/`, `app/dtos/`                                                  |
| Interface Adapters   | `app/dtos/`, `app/apis/`, `app/facades/`, `app/factories/`, `app/exceptions/` |
| Frameworks & Drivers | `app/config/`, `app/utils/`                                                   |

A implementação é orientada a objetos com métodos predominantemente estáticos e de classe: os serviços encapsulam a lógica de negócio em classes sem estado de instância, com uso de mixins e classes base para compartilhar comportamento comum entre camadas, sem herança profunda.

O controle de acesso (RBAC) com três perfis — `ADMIN`, `DISTRIBUTOR` e `SELLER` — é aplicado e validado integralmente no backend. Usuários não são excluídos fisicamente: a remoção é feita por inativação (`is_active = FALSE`), preservando o histórico e os vínculos com pedidos.

## 🗂️ Estruturação

```
viva-control-backend/
├── app/
│   ├── apis/
│   │   ├── auth/
│   │   ├── customer/
│   │   ├── distributor_stock/
│   │   ├── order/
│   │   ├── payment_method/
│   │   ├── product/
│   │   └── user/
│   ├── config/
│   ├── dtos/
│   │   └── mixin/
│   ├── exceptions/
│   │   └── base/
│   ├── facades/
│   ├── factories/
│   ├── models/
│   │   └── mixin/
│   ├── services/
│   │   └── base/
│   └── utils/
├── docs/
├── fixtures/
├── migrations/
├── static/
└── tests/
```

### 📁 `app/`

Código-fonte principal.

#### 📁 `apis/`

Camada de **interface adapters** (adaptadores de interface) — namespaces e resources do Flask-RESTX. Cada subpacote organiza um namespace em `models.py` (modelos Flask-RESTX expostos ao Swagger) e um ou mais módulos `resources.py` (resources com as rotas e os decorators de validação, documentação e proteção JWT). Namespaces com múltiplos perfis, como `user/`, subdividem os resources em subpacotes por perfil. Não contém lógica de negócio: delega toda operação ao serviço correspondente.

#### 📁 `config/`

Configuração e inicialização da aplicação:

- 📄 `paths.py` — Constantes de caminhos do sistema de arquivos.
- 📄 `environs.py` — Variáveis de ambiente lidas via `os.environ`, com valores padrão para desenvolvimento.
- 📄 `setup.py` — Inicializa as extensões Flask e semeia o banco com os dados iniciais.

#### 📁 `dtos/`

Estruturas de dados que tipam os payloads trafegados entre camadas: entradas e saídas da API (`input.py`, `output.py`) e objetos de comunicação interna entre serviços e adaptadores (`internal.py`).

#### 📁 `exceptions/`

Hierarquia de exceções HTTP da aplicação.

#### 📁 `facades/`

Camada de fachadas de uso geral — simplificam e centralizam interfaces complexas para o restante da aplicação.

#### 📁 `factories/`

Classes de fábrica que produzem objetos reutilizáveis a partir dos parâmetros especificados.

#### 📁 `models/`

Camada de **entities** (entidades) — modelos SQLAlchemy.

#### 📁 `services/`

Camada de **use cases** (casos de uso) — classes com métodos estáticos e de classe que encapsulam as regras de cada domínio e operam sobre os modelos. O subpacote `base/` define a classe abstrata `UserService`, compartilhada pelos serviços de usuário com perfis distintos.

#### 📁 `utils/`

Utilitários transversais sem vínculo com um domínio específico.

### 📁 `docs/`

Documentação técnica do projeto: modelo de dados, visão do produto e outras especificações.

### 📁 `fixtures/`

Dados iniciais carregados por `config/setup.py` na primeira inicialização da aplicação, caso os registros ainda não existam no banco.

### 📁 `migrations/`

Gerenciado pelo Flask-Migrate, armazena os scripts de migração do banco no diretório 📁 `versions/`.

### 📁 `static/`

Ativos estáticos do projeto.

### 📁 `tests/`

Suíte de testes automatizados.

## 📚 Referências

- Clean Architecture — Uma abordagem baseada em princípios. Medium, disponível em: [medium.com/@gabrielfernandeslemos/clean-architecture-uma-abordagem-baseada-em-princípios-bf9866da1f9c](https://medium.com/@gabrielfernandeslemos/clean-architecture-uma-abordagem-baseada-em-princípios-bf9866da1f9c).
- O que exatamente é Clean Architecture (Arquitetura Limpa)? Como e onde usar? Stack Overflow em Português, disponível em: [pt.stackoverflow.com/questions/441073](https://pt.stackoverflow.com/questions/441073/o-que-exatamente-%C3%A9-clean-architecture-arquitetura-limpa-como-e-onde-usar).
- Sweet Server. GitHub, disponível em: [github.com/pedrovitorsilva/sweet-server](https://github.com/pedrovitorsilva/sweet-server).
