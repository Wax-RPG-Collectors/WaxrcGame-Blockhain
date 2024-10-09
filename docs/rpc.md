# Servidor RPC

O servidor RPC permite a interação com a blockchain através de chamadas de procedimento remoto (RPC).

## Endpoints

### `/rpc`

Endpoint principal para chamadas RPC.

## Métodos RPC

### `get_blockchain`

Retorna a cadeia de blocos.

### `generate_block`

Gera um novo bloco minerando na fase PoW, PoS ou PoG conforme necessário.

### `get_balance`

Retorna o saldo da carteira.

### `create_transaction`

Cria uma nova transação.

### `add_node`

Adiciona um novo nó.

### `get_nodes`

Retorna a lista de nós.

### `synchronize`

Sincroniza a cadeia com outros nós.

### `generate_addresses`

Gera novos endereços a partir de uma chave privada.

### `create_token`

Cria um novo token.

### `get_token_balance`

Retorna o saldo de um token.

### `transfer_token`

Transfere tokens de um endereço para outro.

### `mine_pending_transactions`

Minera as transações pendentes.

### `confirm_transaction`

Confirma uma transação com base no hash fornecido.