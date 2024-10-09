# Bloco

A classe `Block` representa um bloco na blockchain.

## Atributos

- `index`: Índice do bloco na cadeia.
- `previous_hash`: Hash do bloco anterior.
- `timestamp`: Timestamp de criação do bloco.
- `data`: Dados armazenados no bloco.
- `version`: Versão do bloco.
- `nonce`: Nonce usado no Proof-of-Work.
- `hash`: Hash do bloco.

## Métodos

### `__init__(self, index, previous_hash, timestamp, data, version, nonce=0)`

Inicializa um novo bloco com os parâmetros fornecidos.

### `calculate_hash(self)`

Calcula o hash do bloco.

### `__repr__(self)`

Retorna uma representação em string do bloco.