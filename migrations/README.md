## 🗃️ Migrações do Banco de Dados

Este diretório foi criado com a extensão `Flask-Migrate`, a partir do comando:

```bash
flask db init
```

Ele contém o controle de versionamento do esquema do banco de dados utilizado na aplicação.

Para criar ou aplicar alterações no banco, siga as orientações abaixo:

### 🔄 Criar Arquivo de Migração

Sempre que houver mudanças nos modelos (herdados de `db.Model`), execute:

```bash
flask db migrate -m "descrição da alteração"
```

A descrição é incorporada ao nome do arquivo gerado em `versions/`, tornando o histórico de migrações legível sem precisar abrir cada script. Pode ser necessário ajustá-lo manualmente caso o Alembic não detecte alguma modificação.

### ⬆️ Aplicar Alterações ao Banco

Depois de preparar os scripts, use o comando a seguir para atualizar o banco de dados:

```bash
flask db upgrade
```

---

## 📐 Princípios da Modelagem

O esquema foi projetado sobre os princípios de normalização relacional até a **3ª Forma Normal (3FN)**, com desnormalizações deliberadas e documentadas onde o custo operacional justifica o desvio.

### Normalização até a 3FN

| Forma Normal | Regra aplicada                                                          | Como se manifesta no esquema                                                                                                                                           |
| ------------ | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1FN          | Valores atômicos; sem grupos repetidos                                  | Cada coluna armazena um único valor — `document_type` separa o tipo do número; itens de pedido estão em `order_items`, não em colunas repetidas dentro de `orders`.    |
| 2FN          | Atributos dependem da chave completa; sem dependências parciais         | Toda tabela tem chave primária simples (`id`), eliminando a possibilidade de dependências parciais por construção.                                                     |
| 3FN          | Sem dependências transitivas; atributos não-chave dependem apenas da PK | `suggested_price` vive em `products`, não em `distributor_stocks`; `name` do cliente vive em `customers`, não em `orders` — nenhum atributo não-chave determina outro. |

### Desnormalizações Deliberadas

Um grupo de campos viola a 3FN conscientemente, com justificativa registrada:

**Colunas de escopo propagadas** — `distributor_id` e `seller_id` aparecem em `customers` e `orders` mesmo que a relação entre vendedor e distribuidor já exista via `distributor_id` em `users`. A propagação evita JOINs recursivos na hierarquia a cada consulta de escopo de acesso, mantendo as queries de isolamento multi-tenant simples e diretas.

### Demais Convenções

| Convenção                         | Decisão                                                                                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hierarquia extensível             | `users.distributor_id` é auto-referência; novos níveis (ex.: gerente) não exigem alteração de schema — apenas um novo valor de `role`.                                             |
| Catálogo global, estoque local    | Produto cadastrado uma vez em `products`; posição de estoque e mínimo controlados por distribuidor em `distributor_stocks` com `UNIQUE(product_id, distributor_id)`.               |
| Snapshot de preço                 | `order_items.unit_price` pode diferir de `products.suggested_price`; o valor fixado na venda é o que vale.                                                                         |
| Soft delete em usuários           | Registros de usuários nunca são excluídos fisicamente — inativação via `is_active = FALSE` preserva histórico e integridade referencial.                                           |
| Enums em UPPERCASE                | Valores de `role` e `status` em inglês maiúsculo (`ADMIN`, `DISTRIBUTOR`, `SELLER`, `PENDING` etc.) evitam acoplamento com locale e facilitam comparações case-sensitive no banco. |
| Hash de senha de comprimento fixo | `password_hash CHAR(60)` — o algoritmo scrypt é utilizado para hash de senha; `CHAR` evita armazenamento de padding variável.                                                      |
