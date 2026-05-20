# Viva Control — Documento de Visão do MVP

<br />

## 1. Introdução

### 1.1 Finalidade

Este documento define o escopo do MVP do Viva Control. O objetivo é especificar o mínimo necessário para colocar o sistema em operação com segurança: autenticação com três perfis distintos, cadastros centrais de produtos, clientes e vendedores, um fluxo de pedido completo com validação e baixa de estoque, e bloqueio automático de venda para clientes inadimplentes.

### 1.2 Escopo

O MVP cobre:

- Autenticação de usuários (login por e-mail e senha, logout).
- Controle de acesso por perfil: ADMIN, DISTRIBUTOR e SELLER.
- Cadastro global de produtos com preço sugerido de venda.
- Controle de estoque e estoque mínimo por distribuidor.
- Cadastro de clientes vinculados a vendedores.
- Cadastro de vendedores e usuários do sistema.
- Criação de pedidos com validação de estoque, desconto, parcelamento e meio de pagamento.
- Ciclo de vida do pedido: criação (com baixa de estoque imediata), entrega e confirmação de pagamento.
- Bloqueio de venda para clientes com pagamento vencido em aberto.

Ficam fora do MVP: app mobile, PWA, sincronização offline, notificações push, relatórios analíticos, gráficos e KPIs, metas e comissões, integrações externas (WhatsApp, Pix, boleto, nota fiscal), prestação de contas e despesas de viagem. Esses itens pertencem a versões futuras do produto.

### 1.3 Definições, Acrônimos e Abreviações

| Termo       | Significado                                                                                                |
| ----------- | ---------------------------------------------------------------------------------------------------------- |
| MVP         | Minimum Viable Product — Versão mínima de um produto, incluindo apenas as funcionalidades primordiais      |
| RBAC        | Role-Based Access Control — Controle de acesso baseado em perfis                                           |
| SKU         | Stock Keeping Unit — Identificador único de produto no estoque                                             |
| CRUD        | Create, Read, Update, Delete — Operações básicas sobre um registro                                         |
| CPF         | Cadastro de Pessoa Física — Documento de identificação de pessoa física no Brasil                          |
| CNPJ        | Cadastro Nacional da Pessoa Jurídica — Documento de identificação de empresa no Brasil                     |
| ADMIN       | Perfil de administrador do sistema com acesso irrestrito, criado automaticamente na primeira inicialização |
| DISTRIBUTOR | Perfil do gestor da distribuidora, com acesso total ao próprio sistema e a todos os seus vendedores        |
| SELLER      | Perfil de vendedor, com acesso restrito aos próprios clientes, pedidos e cobranças                         |
| JWT         | JSON Web Token — Token de autenticação gerado no login e enviado em cada requisição subsequente            |

### 1.4 Referências

- Sistema Web de Gestão para Distribuidor — Briefing Técnico V1.

<br />

## 2. Posicionamento

### 2.1 Oportunidade de Negócio

Distribuidoras de pequeno e médio porte operam hoje com controles fragmentados: pedidos anotados em caderno ou enviados por WhatsApp, cobranças gerenciadas em planilha e nenhuma visibilidade centralizada sobre clientes inadimplentes. Essa dispersão gera pedidos perdidos, venda para clientes em aberto e conflito de dados entre vendedores que compartilham a mesma listagem sem separação. O Viva Control centraliza essa operação em um único sistema web, com visibilidade de dados restrita ao perfil do usuário logado e regras de negócio aplicadas diretamente no backend.

### 2.2 Descrição do Problema

|                           |                                                                                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **O problema de**         | Gestão fragmentada de pedidos, cobranças e clientes em ferramentas desconectadas                                                         |
| **Afeta**                 | Gestores de distribuidoras e vendedores externos                                                                                         |
| **Cujo impacto é**        | Perda de pedidos, venda para inadimplentes, ausência de rastreabilidade e conflito de dados entre vendedores                             |
| **Uma boa solução seria** | Um sistema único com controle de acesso por perfil, fluxo de pedido validado e bloqueio automático de venda por inadimplência do cliente |

### 2.3 Sentença de Posição do Produto

|                    |                                                                                                                                        |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Para**           | Distribuidoras de pequeno e médio porte com equipe comercial externa                                                                   |
| **Que**            | Precisam controlar pedidos, estoque, cobranças e clientes de forma organizada e segura                                                 |
| **O Viva Control** | É um sistema de gestão web para distribuidor                                                                                           |
| **Que**            | Centraliza vendas, estoque e cobranças com segregação de dados por vendedor e regras de negócio aplicadas e validadas no backend       |
| **Diferente de**   | Planilhas e grupos de WhatsApp usados informalmente para gestão comercial                                                              |
| **Nosso produto**  | Aplica as regras da operação: bloqueio por inadimplência, baixa automática de estoque e visibilidade restrita ao escopo de cada perfil |

<br />

## 3. Partes Envolvidas

### 3.1 Resumo dos Envolvidos

| Nome                      | Descrição                                         | Responsabilidade                                                                 |
| ------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------- |
| Equipe de Desenvolvimento | Responsáveis pela construção do sistema           | Implementação, testes e entrega das funcionalidades                              |
| Gestor da Distribuidora   | Dono ou gestor da operação                        | Validação dos fluxos de negócio, cadastro inicial de dados e aceite das entregas |
| Vendedores                | Equipe comercial que usará o sistema no dia a dia | Feedback de usabilidade e aderência ao fluxo real de vendas                      |

### 3.2 Resumo dos Usuários

| Perfil      | Descrição                                                                                                                                                |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ADMIN       | Administrador do sistema com acesso irrestrito a todos os módulos e dados. Criado automaticamente na primeira inicialização                              |
| DISTRIBUTOR | Gerencia estoque, clientes e pedidos do próprio escopo; consulta produtos, usuários subordinados e meios de pagamento. Perfil do gestor da distribuidora |
| SELLER      | Acesso restrito aos próprios clientes e pedidos; consulta de produtos e meios de pagamento disponíveis para compor pedidos                               |

### 3.3 Principais Necessidades dos Usuários

| Necessidade                                                                    | Perfil              | Prioridade |
| ------------------------------------------------------------------------------ | ------------------- | ---------- |
| Criar pedidos com validação de estoque em tempo real                           | DISTRIBUTOR, SELLER | Alta       |
| Visualizar apenas os próprios clientes e pedidos                               | SELLER              | Alta       |
| Bloquear automaticamente a venda para clientes com pagamento vencido em aberto | DISTRIBUTOR, SELLER | Alta       |
| Cadastrar e gerenciar usuários, produtos e meios de pagamento                  | ADMIN               | Alta       |
| Gerenciar estoque e cadastrar clientes                                         | DISTRIBUTOR         | Alta       |
| Registrar entrega e confirmação de pagamento dos pedidos                       | DISTRIBUTOR, SELLER | Alta       |
| Consultar produtos disponíveis para montar pedidos                             | SELLER              | Média      |
| Identificar produtos com estoque abaixo do mínimo configurado                  | DISTRIBUTOR         | Média      |

<br />

## 4. Descrição da Solução

### 4.1 Perspectiva do Produto

O MVP entrega o núcleo operacional da distribuidora: usuários autenticados, organizados em três perfis com permissões bem definidas, operando sobre cadastros centrais de produtos, clientes e vendedores, com um fluxo de pedido completo — da criação à confirmação de pagamento — protegido por validações de estoque e inadimplência.

A estrutura do MVP é composta por quatro camadas:

1. **Autenticação** — quem pode entrar.
2. **Autorização (RBAC)** — o que cada perfil pode ver e fazer.
3. **Cadastros centrais** — as entidades que sustentam os módulos de venda.
4. **Fluxo de pedido** — criação validada com baixa de estoque imediata e controle de pagamento integrado ao status.

### 4.2 Resumo dos Recursos

| Recurso                                           | Benefício                                                                         |
| ------------------------------------------------- | --------------------------------------------------------------------------------- |
| Login com controle de acesso por perfil           | Cada usuário vê e opera apenas o que é de sua responsabilidade                    |
| Cadastro global de produtos com preço sugerido    | Produto único no catálogo; preço pode ser ajustado pelo usuário na hora da venda  |
| Estoque e mínimo controlados por distribuidor     | Cada distribuidora controla sua própria posição de estoque independentemente      |
| Cadastro de clientes vinculado ao vendedor        | Cada vendedor enxerga apenas sua própria carteira, sem acesso aos dados de outros |
| Fluxo de pedido com validação de estoque          | Impede a venda acima do estoque disponível no momento da criação                  |
| Baixa de estoque na criação do pedido             | Estoque reservado imediatamente, impedindo sobrevenda entre pedidos simultâneos   |
| Status de pagamento integrado ao pedido           | Sem tabela separada de cobranças — o pedido concentra entrega e pagamento         |
| Bloqueio por inadimplência                        | Impede novo pedido enquanto houver pagamento vencido em aberto para o cliente     |
| Preço fixado no momento da venda                  | O valor do item no pedido não muda caso o preço sugerido do produto seja alterado |
| Desconto percentual e meio de pagamento no pedido | Permite registrar condições comerciais reais aplicadas na venda                   |

<br />

## 5. Recursos do MVP

### 5.1 Autenticação

- Login por e-mail e senha.
- Senha armazenada com hash scrypt (nunca em texto plano).
- Autenticação via par de tokens JWT: `access_token` (validade padrão 15 minutos, configurável via `JWT_ACCESS_TOKEN_EXPIRATION_IN_MINUTES`) emitido junto com `refresh_token` (validade padrão 30 dias, configurável via `JWT_REFRESH_TOKEN_EXPIRATION_IN_DAYS`); o `access_token` expirado pode ser renovado via `POST /auth/refresh`, autenticado pelo `refresh_token`, sem necessidade de novo login.
- Logout manual por descarte local dos tokens; sem endpoint de logout nem revogação server-side.
- HTTPS obrigatório em todos os ambientes a partir do deploy em produção.

### 5.2 Controle de Acesso (RBAC)

O perfil de cada usuário é definido por um campo `role` do tipo enumerado diretamente no registro de usuário, com três valores possíveis: `ADMIN`, `DISTRIBUTOR` e `SELLER`. Essa abordagem mantém o modelo simples e adequado ao escopo do MVP.

#### 5.2.1 Escopos por perfil

| Perfil      | Módulos Acessíveis                                                                                       | Operações                                                                                                                                       |
| ----------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| ADMIN       | Todos os módulos e dados do sistema, sem restrição de escopo                                             | CRUD de usuários, produtos e meios de pagamento; R de estoque, clientes e pedidos                                                               |
| DISTRIBUTOR | Estoque, clientes e pedidos do próprio escopo; R de usuários subordinados, produtos e meios de pagamento | CRUD de estoque próprio; CRUD de clientes e pedidos cadastrados por si; CRU de clientes e pedidos cadastrados por seus vendedores; R dos demais |
| SELLER      | Produtos (leitura), meios de pagamento (leitura), clientes próprios, pedidos próprios                    | R de produtos e meios de pagamento; CRUD de clientes e pedidos cadastrados por si                                                               |

#### 5.2.2 Regras

- As permissões são validadas no backend. Nenhuma regra de acesso reside exclusivamente no frontend.
- O ADMIN não está sujeito a filtros de escopo; tem CRUD sobre usuários, produtos e meios de pagamento e pode consultar (R) qualquer registro de estoque, cliente e pedido.
- O SELLER não consegue acessar dados de outro vendedor via API, independente do endpoint chamado ou dos parâmetros enviados na requisição.
- Apenas o ADMIN pode criar, editar e inativar usuários (DISTRIBUTOR e SELLER), produtos e meios de pagamento. O DISTRIBUTOR pode consultar os usuários vinculados ao seu escopo.
- O DISTRIBUTOR pode criar, editar e inativar clientes e pedidos cadastrados por si. Para clientes e pedidos cadastrados por seus vendedores, pode criar, ler e editar, mas não inativar.
- O SELLER pode criar, editar e inativar apenas os clientes e pedidos cadastrados por si.
- Registros não são excluídos fisicamente: a remoção é feita por inativação via `is_active = FALSE`. O registro sai das listagens operacionais, mas permanece no banco, preservando o histórico e os vínculos com pedidos.
- Acessos a recursos não autorizados retornam HTTP 403.

### 5.3 Cadastro de Produtos

- Campos: nome, SKU/código, descrição e preço sugerido de venda.
- Produto é global — não está vinculado a um distribuidor específico.
- CRUD completo restrito ao ADMIN.
- DISTRIBUTOR e SELLER podem apenas consultar produtos.
- No momento da venda, o usuário pode ajustar o preço unitário do item ou utilizar o preço sugerido; o valor aplicado é gravado em `order_items.unit_price`.
- Estoque e estoque mínimo são controlados por distribuidor na tabela `distributor_stocks`, não no cadastro global do produto.
- CRUD de estoque restrito ao DISTRIBUTOR; ADMIN e SELLER podem apenas consultar.
- O sistema identifica produtos com estoque baixo quando `current_quantity <= minimum_quantity` para o distribuidor logado.
- O endpoint `GET /api/products/low-stock` lista os produtos nessa condição. Acesso restrito ao DISTRIBUTOR; ADMIN também pode consultar.

### 5.4 Cadastro de Clientes

- Campos: nome/razão social, CPF/CNPJ, telefone, endereço, vendedor responsável, data de nascimento (opcional) e observações.
- Tanto o DISTRIBUTOR quanto o SELLER podem cadastrar clientes.
- Se o SELLER cadastrar um cliente, o sistema associa automaticamente ao vendedor logado, sem permitir escolha.
- Se o DISTRIBUTOR cadastrar um cliente, ele pode escolher o vendedor responsável ou deixar o campo sem preenchimento.
- O DISTRIBUTOR visualiza todos os clientes do seu escopo, incluindo os de todos os seus vendedores; pode criar, editar e inativar os clientes cadastrados por si e criar, ler e editar (sem inativar) os clientes cadastrados por seus vendedores.
- O SELLER visualiza, edita e inativa apenas seus próprios clientes.
- O ADMIN pode consultar todos os clientes do sistema.

### 5.5 Cadastro de Vendedores e Usuários

- Campos: nome, e-mail, senha (armazenada com hash) e perfil — `ADMIN`, `DISTRIBUTOR` ou `SELLER`.
- O usuário ADMIN é criado automaticamente na primeira inicialização do sistema com as credenciais definidas via variáveis de ambiente (`ADMIN_EMAIL`, `ADMIN_PASSWORD`). Não é possível criar um segundo ADMIN pela API.
- Todo vendedor (`SELLER`) deve estar vinculado a um distribuidor via `distributor_id`.
- Apenas o ADMIN pode criar, editar e inativar qualquer usuário (DISTRIBUTOR ou SELLER).
- O DISTRIBUTOR pode consultar os usuários (SELLER) vinculados ao seu escopo.
- Login realizado por e-mail e senha.

### 5.6 Pedidos

#### 5.6.1 Criação

- Seleção de cliente, um ou mais produtos com as respectivas quantidades.
- O preço sugerido do produto é apresentado como padrão; o usuário pode ajustá-lo por item antes de confirmar.
- O total bruto do pedido é calculado automaticamente com base nos preços unitários definidos.
- Campos adicionais disponíveis na criação: desconto em percentual (0–100 %), meio de pagamento, data de vencimento do pagamento (`payment_due_date`), número de parcelas (1–10) e observação.
- O valor líquido após desconto é calculado e gravado no pedido: `total_amount × (1 − discount_pct / 100)`.
- O preço unitário de cada item é gravado no pedido e não muda caso o produto seja editado posteriormente.
- O pedido pode ser criado tanto pelo DISTRIBUTOR quanto pelo SELLER.

#### 5.6.2 Validações obrigatórias antes da criação

O backend executa as seguintes verificações, nesta ordem, antes de persistir qualquer dado:

1. O cliente existe e está dentro do escopo do usuário logado.
2. O cliente não possui pagamento vencido em aberto (bloqueio por inadimplência).
3. Todos os produtos têm estoque suficiente para as quantidades solicitadas, verificado em `distributor_stocks` do distribuidor responsável.

Se qualquer uma dessas validações falhar, o pedido não é criado e o sistema retorna a mensagem de erro correspondente.

#### 5.6.3 Fluxo transacional

- **Criação (`PENDING`):** pedido, itens e dedução de estoque persistidos em uma única transação. Se qualquer etapa falhar, toda a operação é revertida.
- **`PENDING → CANCELLED`:** estoque restaurado em `distributor_stocks.current_quantity`; estado terminal.
- **`PENDING → DELIVERED_UNPAID`:** atualização de status; sem movimentação de estoque.
- **`PENDING → DELIVERED_PAID`:** atualização de status (entrega e pagamento simultâneos); sem movimentação de estoque; estado terminal.
- **`DELIVERED_UNPAID → DELIVERED_PAID`:** atualização de status; sem movimentação de estoque; estado terminal.

#### 5.6.4 Status

| Status             | Transições permitidas                               | Descrição                                            |
| ------------------ | --------------------------------------------------- | ---------------------------------------------------- |
| `PENDING`          | → `CANCELLED`, `DELIVERED_UNPAID`, `DELIVERED_PAID` | Pedido criado, aguardando entrega                    |
| `CANCELLED`        | nenhuma (terminal)                                  | Pedido cancelado antes da entrega                    |
| `DELIVERED_UNPAID` | → `DELIVERED_PAID`                                  | Pedido entregue ao cliente; pagamento ainda pendente |
| `DELIVERED_PAID`   | nenhuma (terminal)                                  | Pedido entregue e pagamento confirmado               |

O SELLER pode alterar o status dos próprios pedidos. O DISTRIBUTOR pode alterar o status de qualquer pedido do seu escopo.

### 5.7 Meios de Pagamento

- Tabela de meios de pagamento gerenciada pelo ADMIN.
- DISTRIBUTOR e SELLER podem apenas consultar os meios de pagamento disponíveis.
- Campo: nome (ex.: Dinheiro, PIX, Boleto, Cartão de Crédito).

### 5.8 Bloqueio por Inadimplência

Antes de criar um pedido, o sistema verifica se o cliente possui ao menos um pedido com `status = 'DELIVERED_UNPAID'` e `payment_due_date < data atual`. Se existir, o pedido é bloqueado com a mensagem:

> _"Pedido bloqueado. Cliente possui pagamento vencido em aberto."_

O desbloqueio acontece automaticamente quando o DISTRIBUTOR marca o pedido em aberto como `DELIVERED_PAID`.

<br />

## 6. Requisitos Funcionais

| #    | Funcionalidade                                                                                                                                                       | Prioridade |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| RF01 | Autenticação por e-mail e senha com geração de token JWT                                                                                                             | Alta       |
| RF02 | Logout client-side: descarte local dos tokens sem endpoint de logout nem revogação server-side                                                                       | Alta       |
| RF03 | Controle de acesso por perfil em todas as rotas e ações                                                                                                              | Alta       |
| RF04 | CRUD de usuários (DISTRIBUTOR e SELLER) restrito ao ADMIN; DISTRIBUTOR pode R usuários do seu escopo; SELLER sempre vinculado a um distribuidor via `distributor_id` | Alta       |
| RF05 | CRUD de produtos (global) restrito ao ADMIN; consulta aberta a DISTRIBUTOR e SELLER                                                                                  | Alta       |
| RF06 | CRUD de estoque (`distributor_stocks`) restrito ao DISTRIBUTOR; ADMIN e SELLER podem R; alerta de estoque baixo quando `current_quantity <= minimum_quantity`        | Alta       |
| RF07 | CRUD de clientes por DISTRIBUTOR e SELLER; ADMIN pode R todos; `seller_id` preenchido automaticamente pelo SELLER                                                    | Alta       |
| RF08 | SELLER visualiza, cria, edita e inativa apenas seus próprios clientes                                                                                                | Alta       |
| RF09 | DISTRIBUTOR pode CRUD nos clientes cadastrados por si e CRU nos clientes cadastrados por seus vendedores; ADMIN pode R todos                                         | Alta       |
| RF10 | Criação de pedido com seleção de cliente, produtos e quantidades                                                                                                     | Alta       |
| RF11 | Verificação de inadimplência do cliente antes de criar pedido                                                                                                        | Alta       |
| RF12 | Validação de estoque por distribuidor (`distributor_stocks`) na criação do pedido                                                                                    | Alta       |
| RF13 | Baixa de estoque na criação do pedido; restauração ao cancelar (`CANCELLED`)                                                                                         | Alta       |
| RF14 | Preço unitário do item gravado no momento da venda; pode diferir do preço sugerido                                                                                   | Alta       |
| RF15 | Aplicação de desconto percentual e cálculo de valor líquido no pedido                                                                                                | Alta       |
| RF16 | Seleção de meio de pagamento, data de vencimento e número de parcelas no pedido                                                                                      | Alta       |
| RF17 | Criação de pedido, itens e baixa de estoque persistidos em uma única transação atômica                                                                               | Alta       |
| RF18 | SELLER pode marcar seus próprios pedidos como `DELIVERED_PAID`; DISTRIBUTOR pode marcar qualquer pedido do seu escopo como `DELIVERED_PAID`                          | Alta       |
| RF19 | SELLER visualiza, cria, edita e inativa apenas seus próprios pedidos                                                                                                 | Alta       |
| RF20 | SELLER pode alterar status dos próprios pedidos; DISTRIBUTOR pode alterar status de qualquer pedido do seu escopo                                                    | Média      |
| RF21 | Listagem de produtos com estoque abaixo do mínimo configurado (por distribuidor)                                                                                     | Média      |
| RF22 | SELLER pode inativar seus próprios pedidos; DISTRIBUTOR pode inativar pedidos cadastrados por si (não os de seus vendedores); o histórico é preservado               | Média      |
| RF23 | CRUD de meios de pagamento restrito ao ADMIN; DISTRIBUTOR e SELLER podem R                                                                                           | Média      |

<br />

## 7. Restrições

- Acesso exclusivo via navegador web (Chrome, Firefox, Edge — versões recentes).
- Requer conexão com a internet.
- Banco de dados relacional com suporte a transações ACID.
- Senhas não podem ser armazenadas em texto plano em nenhuma circunstância.
- O sistema não deve operar sem HTTPS em produção.
- As permissões de acesso devem ser aplicadas e validadas no backend; o frontend pode ocultar opções por conveniência, mas nunca é a única barreira.
- Um SELLER não pode visualizar ou alterar dados de outro SELLER em nenhum cenário, incluindo manipulação direta de parâmetros na URL ou no corpo da requisição.

<br />

## 8. Qualidade e Requisitos Técnicos

### 8.1 Implementação

- Interface web responsiva; uso prioritário em desktop.
- Banco relacional com suporte a transações ACID. PostgreSQL é a escolha para produção; SQLite é aceito em desenvolvimento local pelo custo zero de infraestrutura.
- Criação de pedido, itens e baixa de estoque em uma única transação atômica — rollback total em caso de qualquer falha.
- Controle de concorrência: múltiplos vendedores criando pedidos simultaneamente sem inconsistência de estoque.

### 8.2 Performance

- Suporte a até **30 usuários simultâneos**.
- Tempo de resposta máximo para listagens e consultas: **3 segundos**.
- Validação de inadimplência e de estoque: síncrona e transparente para o usuário, sem telas de espera.

### 8.3 Segurança

- HTTPS obrigatório em produção.
- Senhas com hash scrypt.
- `access_token` com expiração de curta duração; não deve ser armazenado em `localStorage` no frontend. `refresh_token`, de validade estendida, deve ser armazenado em `httpOnly cookie` em aplicações web ou em keychain/keystore em clientes nativos.
- O SELLER não deve conseguir acessar dados de outro vendedor via manipulação de parâmetros na URL ou no corpo da requisição.

### 8.4 Usabilidade

- Feedback visual imediato para ações (sucesso, erro, confirmação).
- Validação de formulários com mensagens inline antes do envio ao servidor.
- Busca por nome e código nas listagens de produtos e clientes.

<br />

## 9. Arquitetura e Stack Tecnológica

| Camada         | Tecnologia                           | Justificativa                                                                                                                                                                                                      |
| -------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Banco de Dados | SQLite (dev) / PostgreSQL (produção) | SQLite elimina a necessidade de infraestrutura adicional durante o desenvolvimento; PostgreSQL oferece suporte completo a transações ACID e row-level locking, sendo a escolha natural para o ambiente de produção |
| Backend        | Python + Flask + Flask-RESTX         | Stack leve e produtivo para APIs REST; Flask-RESTX adiciona geração automática de documentação Swagger e organização dos recursos em blueprints; SQLAlchemy atua como ORM e gerencia as transações do banco        |
| Frontend       | React-Admin (Node.js)                | Framework opinionado para interfaces administrativas: listagem, formulário, filtro, paginação e CRUD funcionam com configuração mínima, o que se encaixa bem no perfil de telas do Viva Control                    |

### 9.1 Comunicação entre Camadas

- Frontend consome a API REST exposta pelo backend via HTTPS.
- Autenticação via par de tokens JWT: o `access_token` é emitido no login junto com o `refresh_token` e enviado no header `Authorization: Bearer` em todas as requisições subsequentes; quando expirado, pode ser renovado via `POST /auth/refresh`, autenticado pelo `refresh_token`, sem novo login.
- O backend valida o token e o perfil do usuário antes de processar qualquer operação — as regras de RBAC residem integralmente no backend, nunca apenas no frontend.
- A documentação da API é gerada automaticamente pelo Flask-RESTX e fica disponível via Swagger UI no endpoint `/`.
