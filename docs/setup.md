# Compilação e Nodes

Esta seção descreve como compilar o projeto, criar nodes e ativar a rede principal e a testnet.

## Compilação

Para compilar o projeto, siga os passos abaixo:

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

4. Compile a aplicação (se necessário):
    ```sh
    pyinstaller --onefile main.py
    ```

## Criação de Nodes

Para criar nodes, siga os passos abaixo:

1. Inicie o servidor RPC em cada máquina que será um node:
    ```sh
    python -m rpc.server
    ```

2. Adicione os nodes à rede usando o método RPC `add_node`:
    ```sh
    curl -X POST http://127.0.0.1:8332/rpc -H "Content-Type: application/json" -d '{"method": "add_node", "params": ["http://ip-do-node:8332"]}'
    ```

## Ativação da Rede Principal e Testnet

### Rede Principal

Para ativar a rede principal, siga os passos abaixo:

1. Configure o arquivo de configuração para a rede principal (`config_mainnet.py`):
    ```python
    # config_mainnet.py
    MAX_SUPPLY = 21000000
    COINS_PER_BLOCK = 50
    BLOCKS_BEFORE_POG = 100
    P2P_PORT = 8333
    RPC_PORT = 8332
    BLOCKCHAIN_URL = "http://mainnet.blockchain.url"
    CONTRACT_ADDRESS = "0xMainnetContractAddress"
    CONTRACT_ABI = "MainnetContractABI"
    ```

2. Inicie o servidor RPC com a configuração da rede principal:
    ```sh
    python -m rpc.server --config config_mainnet.py
    ```

### Testnet

Para ativar a testnet, siga os passos abaixo:

1. Configure o arquivo de configuração para a testnet (`config_testnet.py`):
    ```python
    # config_testnet.py
    MAX_SUPPLY = 21000000
    COINS_PER_BLOCK = 50
    BLOCKS_BEFORE_POG = 100
    P2P_PORT = 18333
    RPC_PORT = 18332
    BLOCKCHAIN_URL = "http://testnet.blockchain.url"
    CONTRACT_ADDRESS = "0xTestnetContractAddress"
    CONTRACT_ABI = "TestnetContractABI"
    ```

2. Inicie o servidor RPC com a configuração da testnet:
    ```sh
    python -m rpc.server --config config_testnet.py
    ```

## Notas

- Certifique-se de que todas as dependências estão instaladas e que o código está funcionando corretamente antes de compilar a aplicação.
- A configuração da rede principal e testnet deve ser feita com cuidado para evitar conflitos de porta e outros problemas de rede.