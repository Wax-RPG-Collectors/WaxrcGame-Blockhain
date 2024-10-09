class TestnetConfig:
    NAME = "CryptoGameCoin Testnet"
    TICKER = "CGCT"
    MAX_SUPPLY = 1000000
    RPC_PORT = 18332
    P2P_PORT = 18333
    BLOCKCHAIN_URL = "http://127.0.0.1:8545"  # URL do nó da blockchain de teste
    CONTRACT_ADDRESS = "0xYourTestnetContractAddress"  # Endereço do contrato inteligente na testnet
    CONTRACT_ABI = [...]  # ABI do contrato inteligente
    COINS_PER_BLOCK = 10
    BLOCKS_BEFORE_POG = 100