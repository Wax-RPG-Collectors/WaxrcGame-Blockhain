### `transfer_token(self, symbol, from_address, to_address, amount)`

Transfere tokens de um endereço para outro.

### `create_transaction(self, sender, recipient, amount)`

Cria uma nova transação.

### `calculate_transaction_fee(self, amount)`

Calcula a taxa de transação.

### `calculate_token_creation_fee(self)`

Calcula a taxa de criação de tokens com base na dificuldade da rede.

### `calculate_game_creation_fee(self)`

Calcula a taxa de criação de jogos com base na dificuldade da rede.

### `mine_pending_transactions(self)`

Minera as transações pendentes.

### `confirm_transaction(self, transaction_hash)`

Confirma uma transação com base no hash fornecido.

### `create_game(self, game_id, name, logo, url)`

Cria um novo jogo com o ID, nome, logo e URL fornecidos.

### `update_game_time(self, game_id, time_played)`

Atualiza o tempo jogado para o jogo com o ID fornecido.

### `check_game_eligibility(self, game_id)`

Verifica se o jogo com o ID fornecido é elegível para receber a recompensa (mínimo de 24 horas ativo).

### `process_transaction(self, transaction)`

Processa uma transação e define se é relacionada a jogos (PoG), Proof-of-Work (PoW) ou Proof-of-Stake (PoS).

### `confirm_transaction(self, transaction_hash, fast=False)`

Confirma uma transação com base no hash fornecido. Se `fast` for `True`, confirma 3x mais rápido.

### `sign_transaction(self, transaction, private_key)`

Assina uma transação com a chave privada fornecida.

### `verify_transaction_signature(self, transaction)`

Verifica a assinatura de uma transação.

### `add_transaction(self, transaction, private_key)`

Adiciona uma transação assinada à mempool.

### `calculate_transaction_fee(self, amount, fast=False)`

Calcula a taxa de transação com base no valor e se é uma transação rápida.

### `calculate_coins_per_block(self)`

Calcula a recompensa por bloco com base na demanda e na dificuldade da rede.

### `get_current_supply(self)`

Retorna o fornecimento atual de tokens.

### `get_max_supply(self)`

Retorna o fornecimento máximo de tokens.