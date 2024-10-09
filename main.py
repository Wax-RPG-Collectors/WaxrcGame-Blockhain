import sys
import os
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
from game.game_integration import GameIntegration
from config.settings import Config
from config.testnet_settings import TestnetConfig
import threading
import rpc.server

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'testnet':
        config = TestnetConfig
    else:
        config = Config

    print(f"Starting {config.NAME} ({config.TICKER})")
    print(f"Max Supply: {config.MAX_SUPPLY}")
    print(f"RPC Port: {config.RPC_PORT}")
    print(f"P2P Port: {config.P2P_PORT}")

    blockchain = Blockchain(config)
    wallet = Wallet()
    game_integration = GameIntegration(blockchain, wallet)
    
    print(f"New wallet created with address: {wallet.address}")

    game_integration.reward_player("player1", 100)
    print("Player rewarded. Current wallet balance:", wallet.balance)
    print("Blockchain latest block data:", blockchain.chain[-1].data)

    # Criar e assinar uma transação
    recipient_address = "GaxRecipientAddress"
    transaction = wallet.create_transaction(recipient_address, 50)
    print(f"Transaction created and signed: {transaction.__dict__}")

    # Adicionando blocos para teste
    for i in range(1, 105):
        blockchain.add_block(f"Block {i} data")
        print(f"Block {i} added with hash: {blockchain.chain[-1].hash}")

    # Verificando a integridade da blockchain
    print("Blockchain valid:", blockchain.is_chain_valid())

    # Iniciar o servidor RPC em uma thread separada
    rpc_thread = threading.Thread(target=rpc.server.app.run, kwargs={'port': config.RPC_PORT})
    rpc_thread.start()

    # Sincronizar blockchain com peers
    blockchain.synchronize()

    # Adicionar um validador e um nó para teste
    blockchain.add_validator(wallet.address)
    blockchain.add_node(wallet.address)
    print("Nodes in the network:", blockchain.get_nodes())

def run_daemon():
    pid = os.fork()
    if pid > 0:
        # Exit parent process
        sys.exit(0)
    # Decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)
    # Do second fork
    pid = os.fork()
    if pid > 0:
        # Exit from second parent
        sys.exit(0)
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'w') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())
    main()

if __name__ == "__main__":
    main()