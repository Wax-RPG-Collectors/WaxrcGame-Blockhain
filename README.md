# Crypto Game Project

Este projeto é uma implementação básica de uma blockchain e carteira em Python, com integração para jogos.

## Estrutura do Projeto

- `blockchain/`: Contém a lógica principal da blockchain.
- `wallet/`: Contém a lógica para a criação e gerenciamento de carteiras.
- `network/`: Contém a lógica para a comunicação entre nós da rede.
- `game/`: Contém a lógica específica para integração com jogos.
- `config/`: Contém as configurações básicas da moeda.
- `tests/`: Contém os testes unitários e de integração.
- `scripts/`: Contém scripts auxiliares para tarefas comuns.
- `main.py`: Arquivo principal para iniciar a aplicação.

## Configurações da Moeda

- Nome: CryptoGameCoin
- Ticker: CGC
- Suprimento Máximo: 1,000,000
- Porta RPC: 8332
- Porta P2P: 8333
- Moedas por Bloco: 10
- Blocos antes de Proof-of-Game: 100

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/crypto-game-project.git
    cd crypto-game-project
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure as variáveis no arquivo `config/settings.py` conforme necessário.

5. Execute a aplicação:
    ```sh
    python main.py
    ```

## Uso

- Para adicionar um bloco:
    ```sh
    curl -X POST http://127.0.0.1:8332/rpc -H "Content-Type: application/json" -d '{"method": "add_block", "params": ["Block data"]}'
    ```

- Para obter a blockchain:
    ```sh
    curl -X POST http://127.0.0.1:8332/rpc -H "Content-Type: application/json" -d '{"method": "get_blockchain", "params": []}'
    ```

- Para adicionar um nó:
    ```sh
    curl -X POST http://127.0.0.1:8332/rpc -H "Content-Type: application/json" -d '{"method": "add_node", "params": ["Node address"]}'
    ```

- Para sincronizar a blockchain:
    ```sh
    curl -X POST http://127.0.0.1:8332/rpc -H "Content-Type: application/json" -d '{"method": "synchronize", "params": []}'
    ```

- Para minerar blocos até o bloco 10000:
    ```sh
    python main.py
    ```

## Testnet

Para configurar e usar a testnet:

1. Configure as variáveis no arquivo `config/testnet_settings.py` conforme necessário.

2. Execute a aplicação na testnet:
    ```sh
    python main.py testnet
    ```

- Para adicionar um bloco na testnet:
    ```sh
    curl -X POST http://127.0.0.1:18332/rpc -H "Content-Type: application/json" -d '{"method": "add_block", "params": ["Block data"]}'
    ```

- Para obter a blockchain na testnet:
    ```sh
    curl -X POST http://127.0.0.1:18332/rpc -H "Content-Type: application/json" -d '{"method": "get_blockchain", "params": []}'
    ```

- Para adicionar um nó na testnet:
    ```sh
    curl -X POST http://127.0.0.1:18332/rpc -H "Content-Type: application/json" -d '{"method": "add_node", "params": ["Node address"]}'
    ```

- Para sincronizar a blockchain na testnet:
    ```sh
    curl -X POST http://127.0.0.1:18332/rpc -H "Content-Type: application/json" -d '{"method": "synchronize", "params": []}'
    ```

- Para minerar blocos até o bloco 10000 na testnet:
    ```sh
    python main.py testnet
    ```

## Interação com o Contrato Inteligente

Para interagir com o contrato inteligente, você pode usar as funções `add_validator`, `add_node` e `get_nodes` da classe `Blockchain`.

### Exemplo de Uso

```python
from blockchain.blockchain import Blockchain
from config.settings import Config

# Inicializar a blockchain com a configuração
blockchain = Blockchain(Config)

# Adicionar um validador
validator_address = "0xValidatorAddress"
blockchain.add_validator(validator_address)

# Adicionar um nó
node_address = "0xNodeAddress"
blockchain.add_node(node_address)

# Obter a lista de nós
nodes = blockchain.get_nodes()
print("Nodes in the network:", nodes)curl -X POST http://127.0.0.1:8332/rpc -H "Content-Type: application/json" -d '{"method": "generate_addresses", "params": ["<private_key_hex>", <count>]}'