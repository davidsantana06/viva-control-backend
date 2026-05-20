# Viva Control — Modelagem do MVP

<br />

## 1. Modelo Conceitual

### Hierarquia de Usuários

| Entidade | Cardinalidade | Entidade | Observação                                                                                                         |
| :------- | :-----------: | :------- | :----------------------------------------------------------------------------------------------------------------- |
| `users`  |  0..1 : 0..N  | `users`  | Um usuário pode ter vários subordinados diretos; o nó raiz não tem distribuidor superior (`distributor_id = NULL`) |

### Cadastros

| Entidade   | Cardinalidade | Entidade             | FK em destaque   | Observação                                                                  |
| :--------- | :-----------: | :------------------- | :--------------- | :-------------------------------------------------------------------------- |
| `users`    |     1 : N     | `distributor_stocks` | `distributor_id` | Cada entrada de estoque pertence a exatamente um distribuidor               |
| `products` |     1 : N     | `distributor_stocks` | `product_id`     | Estoque e quantidade mínima de cada produto são rastreados por distribuidor |
| `users`    |     1 : N     | `customers`          | `distributor_id` | Todo cliente pertence a exatamente um distribuidor (obrigatório)            |
| `users`    |   1 : 0..N    | `customers`          | `seller_id`      | Um vendedor pode ser responsável por zero ou mais clientes (opcional)       |

### Pedidos

| Entidade          | Cardinalidade | Entidade      | FK em destaque      | Observação                                                                 |
| :---------------- | :-----------: | :------------ | :------------------ | :------------------------------------------------------------------------- |
| `payment_methods` |   1 : 0..N    | `orders`      | `payment_method_id` | Um meio de pagamento pode ser usado em vários pedidos (opcional no pedido) |
| `customers`       |     1 : N     | `orders`      | `customer_id`       | Um cliente pode ter vários pedidos ao longo do tempo                       |
| `users`           |     1 : N     | `orders`      | `distributor_id`    | Todo pedido pertence ao escopo de exatamente um distribuidor (obrigatório) |
| `users`           |   1 : 0..N    | `orders`      | `seller_id`         | Um vendedor pode registrar zero ou mais pedidos (opcional)                 |
| `orders`          |     1 : N     | `order_items` | `order_id`          | Um pedido contém um ou mais itens                                          |
| `order_items`     |     N : 1     | `products`    | `product_id`        | Cada item referencia um produto; o preço é fixado no momento da venda      |

<br />

## 2. Modelo Lógico

### 2.1. users

| Column         | Type           | Constraints                  | Descrição                                                                       |
| :------------- | :------------- | :--------------------------- | :------------------------------------------------------------------------------ |
| id             | `INTEGER`      | PK, Not Null, Auto-increment | Identificador único                                                             |
| distributor_id | `INTEGER`      | FK(users.id), Nullable       | Distribuidor ao qual o usuário está vinculado; `NULL` para ADMIN e DISTRIBUTOR  |
| name           | `VARCHAR(50)`  | Not Null                     | Nome completo do usuário                                                        |
| email          | `VARCHAR(255)` | Unique, Not Null             | E-mail de acesso ao sistema; usado como login                                   |
| password_hash  | `CHAR(60)`     | Not Null                     | Hash scrypt da senha; nunca armazenada em texto plano                           |
| role           | `VARCHAR(11)`  | Not Null                     | Perfil do usuário: `ADMIN`, `DISTRIBUTOR` ou `SELLER`                           |
| is_active      | `BOOLEAN`      | Not Null, Default TRUE       | Permite inativar o usuário sem excluir o registro e o histórico vinculado a ele |
| created_at     | `TIMESTAMP`    | Not Null, Default `NOW()`    | Data de criação                                                                 |
| updated_at     | `TIMESTAMP`    | Not Null, Default `NOW()`    | Data da última atualização                                                      |

> **FK:** `users.distributor_id` → `users.id`  
> **CHECK:** `role IN ('ADMIN', 'DISTRIBUTOR', 'SELLER')`  
> Quando `role = 'SELLER'`, `distributor_id` deve ser `NOT NULL` e apontar para o distribuidor responsável. Quando `role = 'DISTRIBUTOR'`, `distributor_id` é `NULL`. Quando `role = 'ADMIN'`, `distributor_id` é `NULL`; o registro é criado automaticamente na primeira inicialização do sistema com as credenciais definidas nas variáveis de ambiente `ADMIN_EMAIL` e `ADMIN_PASSWORD`.

### 2.2. products

| Column          | Type            | Constraints                  | Descrição                                                                       |
| :-------------- | :-------------- | :--------------------------- | :------------------------------------------------------------------------------ |
| id              | `INTEGER`       | PK, Not Null, Auto-increment | Identificador único                                                             |
| name            | `VARCHAR(100)`  | Not Null                     | Nome do produto                                                                 |
| sku             | `VARCHAR(50)`   | Unique, Not Null             | Código SKU do produto                                                           |
| description     | `TEXT`          | Nullable                     | Descrição detalhada do produto                                                  |
| suggested_price | `DECIMAL(15,2)` | Not Null                     | Preço sugerido de venda; pode ser substituído pelo usuário no momento do pedido |
| created_at      | `TIMESTAMP`     | Not Null, Default `NOW()`    | Data de criação                                                                 |
| updated_at      | `TIMESTAMP`     | Not Null, Default `NOW()`    | Data da última atualização                                                      |

> Produto é cadastrado globalmente — sem vínculo direto com distribuidor. Estoque e estoque mínimo são controlados por distribuidor na tabela `distributor_stocks`. O preço sugerido pode ser ajustado pelo usuário no momento da venda; o valor efetivamente aplicado é gravado em `order_items.unit_price` e não muda retroativamente.

### 2.3. distributor_stocks

| Column           | Type            | Constraints                  | Descrição                                                                                 |
| :--------------- | :-------------- | :--------------------------- | :---------------------------------------------------------------------------------------- |
| id               | `INTEGER`       | PK, Not Null, Auto-increment | Identificador único                                                                       |
| product_id       | `INTEGER`       | FK(products.id), Not Null    | Produto ao qual o registro de estoque se refere                                           |
| distributor_id   | `INTEGER`       | FK(users.id), Not Null       | Distribuidor proprietário do estoque                                                      |
| current_quantity | `DECIMAL(15,4)` | Not Null, Default 0          | Quantidade atual em estoque; decrementada na criação do pedido e restaurada ao cancelar   |
| minimum_quantity | `DECIMAL(15,4)` | Not Null, Default 0          | Quantidade mínima configurada; dispara alerta quando `current_quantity` atinge esse valor |
| created_at       | `TIMESTAMP`     | Not Null, Default `NOW()`    | Data de criação                                                                           |
| updated_at       | `TIMESTAMP`     | Not Null, Default `NOW()`    | Data da última atualização                                                                |

> **FK:** `distributor_stocks.product_id` → `products.id`  
> **FK:** `distributor_stocks.distributor_id` → `users.id`  
> **UNIQUE:** `(product_id, distributor_id)` — cada produto tem no máximo um registro de estoque por distribuidor.  
> O sistema considera estoque baixo quando `current_quantity <= minimum_quantity`. O endpoint `GET /api/products/low-stock` retorna os produtos nessa condição para o distribuidor logado.

### 2.4. customers

| Column         | Type          | Constraints                  | Descrição                                                                       |
| :------------- | :------------ | :--------------------------- | :------------------------------------------------------------------------------ |
| id             | `INTEGER`     | PK, Not Null, Auto-increment | Identificador único                                                             |
| distributor_id | `INTEGER`     | FK(users.id), Not Null       | Distribuidor ao qual o cliente pertence; define o escopo de isolamento          |
| seller_id      | `INTEGER`     | FK(users.id), Nullable       | Vendedor responsável; define a visibilidade do cliente para o SELLER            |
| name           | `VARCHAR(50)` | Not Null                     | Nome ou razão social do cliente                                                 |
| document       | `VARCHAR(14)` | Not Null                     | CPF ou CNPJ sem caracteres especiais (máximo 14 dígitos para CNPJ)              |
| document_type  | `VARCHAR(4)`  | Not Null                     | Tipo do documento: `CPF` ou `CNPJ`                                              |
| phone          | `VARCHAR(14)` | Nullable                     | Telefone sem caracteres especiais (máximo 14 dígitos)                           |
| address        | `TEXT`        | Nullable                     | Endereço completo                                                               |
| birth_date     | `DATE`        | Nullable                     | Data de nascimento; opcional, aplica-se principalmente a clientes pessoa física |
| notes          | `TEXT`        | Nullable                     | Observação livre sobre o cliente                                                |
| created_at     | `TIMESTAMP`   | Not Null, Default `NOW()`    | Data de criação                                                                 |
| updated_at     | `TIMESTAMP`   | Not Null, Default `NOW()`    | Data da última atualização                                                      |

> **FK:** `customers.distributor_id` → `users.id`  
> **FK:** `customers.seller_id` → `users.id`  
> **CHECK:** `document_type IN ('CPF', 'CNPJ')`  
> Quando o SELLER cadastra um cliente, o sistema preenche `seller_id` automaticamente com o id do usuário logado e `distributor_id` com o distribuidor do vendedor. Quando o DISTRIBUTOR cadastra um cliente, pode definir qualquer vendedor ativo ou deixar `seller_id` `NULL`. O DISTRIBUTOR visualiza todos os clientes do seu escopo; o SELLER visualiza apenas os clientes onde `seller_id` corresponde ao seu `id`.

### 2.5. payment_methods

| Column     | Type          | Constraints                  | Descrição                                                                 |
| :--------- | :------------ | :--------------------------- | :------------------------------------------------------------------------ |
| id         | `INTEGER`     | PK, Not Null, Auto-increment | Identificador único                                                       |
| name       | `VARCHAR(50)` | Not Null                     | Nome do meio de pagamento (ex.: Dinheiro, PIX, Boleto, Cartão de Crédito) |
| created_at | `TIMESTAMP`   | Not Null, Default `NOW()`    | Data de criação                                                           |
| updated_at | `TIMESTAMP`   | Not Null, Default `NOW()`    | Data da última atualização                                                |

### 2.6. orders

| Column               | Type          | Constraints                      | Descrição                                                                           |
| :------------------- | :------------ | :------------------------------- | :---------------------------------------------------------------------------------- |
| id                   | `INTEGER`     | PK, Not Null, Auto-increment     | Identificador único                                                                 |
| customer_id          | `INTEGER`     | FK(customers.id), Not Null       | Cliente do pedido                                                                   |
| distributor_id       | `INTEGER`     | FK(users.id), Not Null           | Distribuidor responsável pelo escopo do pedido                                      |
| seller_id            | `INTEGER`     | FK(users.id), Nullable           | Vendedor que registrou o pedido; `NULL` quando criado diretamente pelo distribuidor |
| payment_method_id    | `INTEGER`     | FK(payment_methods.id), Nullable | Meio de pagamento selecionado no momento da venda                                   |
| discount_pct         | `INTEGER`     | Not Null, Default 0              | Percentual de desconto aplicado sobre `total_amount`; entre 0 e 100                 |
| payment_installments | `INTEGER`     | Not Null, Default 1              | Número de parcelas do pagamento; entre 1 e 10                                       |
| payment_due_date     | `DATE`        | Not Null                         | Data de vencimento do pagamento                                                     |
| notes                | `TEXT`        | Nullable                         | Observação livre sobre o pedido                                                     |
| status               | `VARCHAR(16)` | Not Null, Default 'PENDING'      | Status atual do pedido                                                              |
| created_at           | `TIMESTAMP`   | Not Null, Default `NOW()`        | Data de criação                                                                     |
| updated_at           | `TIMESTAMP`   | Not Null, Default `NOW()`        | Data da última atualização                                                          |

> **FK:** `orders.customer_id` → `customers.id`  
> **FK:** `orders.distributor_id` → `users.id`  
> **FK:** `orders.seller_id` → `users.id`  
> **FK:** `orders.payment_method_id` → `payment_methods.id`  
> **CHECK:** `status IN ('PENDING', 'CANCELLED', 'DELIVERED_UNPAID', 'DELIVERED_PAID')`  
> **CHECK:** `discount_pct BETWEEN 0 AND 100`  
> **CHECK:** `payment_installments BETWEEN 1 AND 10`
>
> **Campos calculados (não persistidos):** `total_amount` = soma de `order_items.total_price`; `discount_amount` = `total_amount × discount_pct / 100`; `net_amount` = `total_amount − discount_amount`. Calculados dinamicamente como propriedades do modelo a partir dos itens carregados.
>
> Quando o SELLER cria o pedido: `distributor_id = seller.distributor_id`, `seller_id = seller.id`. Quando o DISTRIBUTOR cria: `distributor_id = distributor.id`, `seller_id = NULL`. A criação do pedido, dos itens e a dedução de `distributor_stocks.current_quantity` ocorrem dentro de uma única transação. Se qualquer etapa falhar, toda a operação é revertida.
>
> **Transições de status e impacto no estoque:**
>
> - `PENDING → CANCELLED` — estoque restaurado em `distributor_stocks.current_quantity`; estado terminal.
> - `PENDING → DELIVERED_UNPAID` — sem movimentação de estoque; pagamento ainda pendente.
> - `PENDING → DELIVERED_PAID` — sem movimentação de estoque (entrega e pagamento simultâneos); estado terminal.
> - `DELIVERED_UNPAID → DELIVERED_PAID` — sem movimentação de estoque; pagamento confirmado; estado terminal.
>
> A verificação de inadimplência consulta pedidos com `status = 'DELIVERED_UNPAID'` e `payment_due_date < data atual`.

### 2.7. order_items

| Column     | Type            | Constraints                  | Descrição                                                                                  |
| :--------- | :-------------- | :--------------------------- | :----------------------------------------------------------------------------------------- |
| id         | `INTEGER`       | PK, Not Null, Auto-increment | Identificador único                                                                        |
| order_id   | `INTEGER`       | FK(orders.id), Not Null      | Pedido ao qual o item pertence                                                             |
| product_id | `INTEGER`       | FK(products.id), Not Null    | Produto vendido                                                                            |
| quantity   | `INTEGER`       | Not Null                     | Quantidade vendida; deduzida de `distributor_stocks.current_quantity` na criação do pedido |
| unit_price | `DECIMAL(15,2)` | Not Null                     | Preço unitário aplicado na venda; pode diferir do `suggested_price` do produto             |
| created_at | `TIMESTAMP`     | Not Null, Default `NOW()`    | Data de criação                                                                            |
| updated_at | `TIMESTAMP`     | Not Null, Default `NOW()`    | Data da última atualização                                                                 |

> **FK:** `order_items.order_id` → `orders.id`  
> **FK:** `order_items.product_id` → `products.id`  
> **Campo calculado (não persistido):** `total_price` = `quantity × unit_price`; calculado dinamicamente como propriedade do modelo.
