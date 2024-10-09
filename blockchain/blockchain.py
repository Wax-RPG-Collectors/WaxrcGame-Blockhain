import time
import hashlib
import random
import os
import pyscrypt  # Certifique-se de importar o módulo pyscrypt
from .block import Block
from network.node import Node
from storage.batch_storage import BatchStorage
from web3 import Web3
from eth_account import Account

class Blockchain:
    def __init__(self, config):
        self.config = config
        self.version = "1.0.0"  # Versão da blockchain
        self.storage = BatchStorage()
        self.chain = self.load_blocks_from_batches()
        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_block_to_batch(self.chain[0])
        self.max_supply = config.MAX_SUPPLY
        self.current_supply = 0
        self.difficulty = 4
        self.base_coins_per_block = config.COINS_PER_BLOCK
        self.blocks_before_pog = config.BLOCKS_BEFORE_POG
        self.node = Node(config.P2P_PORT)
        self.batch_size = 10
        self.current_batch = []
        self.pending_transactions = []
        self.tokens = {}  # Dicionário para armazenar tokens
        self.token_creation_fee = 100  # Taxa para criar um token
        self.max_decimals = 18  # Número máximo de decimais para tokens
        self.confirmation_limit = 6  # Limite de confirmações para confirmar envio
        self.transaction_fee = 0.01  # Taxa de transação padrão
        self.validators = {}  # Dicionário para armazenar validadores e seus stakes
        self.games = {}  # Dicionário para armazenar jogos e tempo jogado
        self.fast_confirmation_limit = 2  # Limite de confirmações para transações rápidas

        # Configurar conexão com a blockchain e contrato inteligente
        self.web3 = Web3(Web3.HTTPProvider(config.BLOCKCHAIN_URL))
        self.contract = self.web3.eth.contract(
            address=config.CONTRACT_ADDRESS,
            abi=config.CONTRACT_ABI
        )
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", self.version)

    def get_latest_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def proof_of_game(self, block):
        # Implementar lógica de Proof-of-Game aqui
        total_time_played = sum(game['time_played'] for game in self.games.values())
        if total_time_played == 0:
            raise ValueError("No games with time played available.")
        
        # Selecionar validadores com base no tempo jogado
        selected_validators = random.choices(
            list(self.games.keys()),
            weights=[game['time_played'] for game in self.games.values()],
            k=1
        )
        
        # Dividir a recompensa entre os validadores
        for validator in selected_validators:
            self.validators[validator] += self.coins_per_block * (self.games[validator]['time_played'] / total_time_played)
        
        block.validator = selected_validators[0]
        block.hash = block.calculate_hash()
        return block

    def proof_of_stake(self, block):
        # Selecionar um validador aleatoriamente baseado no stake
        total_stake = sum(self.validators.values())
        if total_stake == 0:
            raise ValueError("No validators with stake available.")
        selected_validator = random.choices(
            list(self.validators.keys()),
            weights=list(self.validators.values())
        )[0]
        block.validator = selected_validator
        block.hash = block.calculate_hash()
        return block

    def calculate_coins_per_block(self):
        # Lógica de recompensa inteligente
        demand_factor = len(self.pending_transactions) / 100  # Exemplo de fator de demanda
        difficulty_factor = self.difficulty / 10
        base_reward = self.base_coins_per_block
        reward = base_reward / (1 + demand_factor * difficulty_factor)
        return max(1, reward)  # Garantir que a recompensa mínima seja 1

    def generate_block(self, data):
        if self.current_supply >= self.max_supply:
            print("Max supply reached. Cannot add more blocks.")
            return

        if len(self.chain) >= 10000:
            print("Block limit reached. Cannot mine more blocks.")
            return

        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), previous_block.hash, time.time(), data, self.version)

        if len(self.chain) % self.blocks_before_pog == 0:
            new_block = self.proof_of_game(new_block)
        elif self.current_supply >= self.max_supply:
            new_block = self.proof_of_stake(new_block)
        else:
            new_block = self.proof_of_work(new_block)

        self.coins_per_block = self.calculate_coins_per_block()
        self.chain.append(new_block)
        self.current_batch.append(new_block)
        if len(self.current_batch) >= self.batch_size:
            self.save_batch_to_storage()
            self.current_batch = []
        self.current_supply += self.coins_per_block

        # Broadcast the new block to peers
        self.node.broadcast_new_block(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_chain_valid():
            self.chain = new_chain
            return True
        return False

    def synchronize(self):
        new_chain = self.node.request_chain()
        if new_chain:
            self.replace_chain(new_chain)

    def save_batch_to_storage(self):
        batch_number = len(os.listdir(self.storage.directory))
        self.storage.save_batch(self.current_batch, batch_number)

    def load_blocks_from_batches(self):
        batches = self.storage.load_batches()
        return [Block(**block_data) for block_data in batches]

    def add_validator(self, validator_address, stake):
        if validator_address in self.validators:
            self.validators[validator_address] += stake
        else:
            self.validators[validator_address] = stake
        tx_hash = self.contract.functions.addValidator(validator_address).transact({'from': self.web3.eth.defaultAccount})
        self.web3.eth.waitForTransactionReceipt(tx_hash)

    def add_node(self, node_address):
        tx_hash = self.contract.functions.addNode(node_address).transact({'from': self.web3.eth.defaultAccount})
        self.web3.eth.waitForTransactionReceipt(tx_hash)

    def get_nodes(self):
        return self.contract.functions.getNodes().call()

    # Métodos para criar e gerenciar tokens
    def create_token(self, name, symbol, initial_supply, decimals):
        if symbol in self.tokens:
            raise ValueError("Token with this symbol already exists.")
        if decimals > self.max_decimals:
            raise ValueError(f"Decimals cannot exceed {self.max_decimals}.")
        token_creation_fee = self.calculate_token_creation_fee()
        if self.current_supply < token_creation_fee:
            raise ValueError("Insufficient balance to pay the token creation fee.")
        self.current_supply -= token_creation_fee
        self.tokens[symbol] = {
            'name': name,
            'symbol': symbol,
            'total_supply': initial_supply,
            'decimals': decimals,
            'balances': {}
        }
        self.tokens[symbol]['balances'][self.web3.eth.defaultAccount] = initial_supply
        self.pending_transactions.append({
            'type': 'token_creation',
            'name': name,
            'symbol': symbol,
            'initial_supply': initial_supply,
            'decimals': decimals,
            'creator': self.web3.eth.defaultAccount
        })

    def get_token_balance(self, symbol, address):
        if symbol not in self.tokens:
            raise ValueError("Token not found.")
        return self.tokens[symbol]['balances'].get(address, 0)

    def transfer_token(self, symbol, from_address, to_address, amount):
        if symbol not in self.tokens:
            raise ValueError("Token not found.")
        if self.tokens[symbol]['balances'].get(from_address, 0) < amount:
            raise ValueError("Insufficient balance.")
        self.tokens[symbol]['balances'][from_address] -= amount
        if to_address in self.tokens[symbol]['balances']:
            self.tokens[symbol]['balances'][to_address] += amount
        else:
            self.tokens[symbol]['balances'][to_address] = amount
        self.pending_transactions.append({
            'type': 'token_transfer',
            'symbol': symbol,
            'from': from_address,
            'to': to_address,
            'amount': amount,
            'fast': True  # Indica que esta é uma transação rápida
        })

    def create_transaction(self, sender, recipient, amount, fast=False):
        transaction_fee = self.calculate_transaction_fee(amount, fast)
        total_amount = amount + transaction_fee
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'fee': transaction_fee,
            'total_amount': total_amount,
            'timestamp': time.time(),
            'fast': fast
        }
        transaction_hash = hashlib.sha256(str(transaction).encode()).hexdigest()
        transaction['hash'] = transaction_hash
        self.pending_transactions.append(transaction)
        return transaction_hash

    def calculate_transaction_fee(self, amount, fast=False):
        # Implementar lógica de taxa de transação inteligente aqui
        base_fee = self.transaction_fee
        difficulty_multiplier = self.difficulty / 10
        fast_multiplier = 3 if fast else 1
        return base_fee * difficulty_multiplier * fast_multiplier

    def calculate_token_creation_fee(self):
        # A taxa de criação de tokens aumenta ou diminui de acordo com a dificuldade da rede
        return self.token_creation_fee * self.difficulty

    def calculate_game_creation_fee(self):
        # A taxa de criação de jogos aumenta ou diminui de acordo com a dificuldade da rede
        return self.token_creation_fee * self.difficulty

    def waxrc_scrypt(self, block):
        target = 2 ** (256 - self.difficulty)
        scrypt_params = {
            'N': 1024,
            'r': 8,
            'p': 1,
            'dkLen': 32
        }
        while int(block.hash, 16) >= target:
            block.nonce += 1
            block.hash = block.calculate_hash()
            scrypt_hash = pyscrypt.hash(password=block.hash.encode('utf-8'), salt=b'salt', **scrypt_params)
            block.hash = hashlib.sha256(scrypt_hash).hexdigest()
        return block

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            return None
        new_block_data = {
            'transactions': self.pending_transactions,
            'miner': miner_address
        }
        new_block = Block(len(self.chain), self.get_latest_block().hash, time.time(), new_block_data, self.version)
        new_block = self.waxrc_scrypt(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def sign_transaction(self, transaction, private_key):
        account = Account.from_key(private_key)
        transaction['signature'] = account.sign_transaction(transaction).signature.hex()
        return transaction

    def verify_transaction_signature(self, transaction):
        sender = transaction['sender']
        signature = transaction['signature']
        transaction_copy = transaction.copy()
        del transaction_copy['signature']
        message_hash = hashlib.sha256(str(transaction_copy).encode()).hexdigest()
        recovered_address = Account.recover_message(message_hash, signature=signature)
        return recovered_address == sender

    def add_transaction(self, transaction, private_key):
        signed_transaction = self.sign_transaction(transaction, private_key)
        if self.verify_transaction_signature(signed_transaction):
            self.pending_transactions.append(signed_transaction)
        else:
            raise ValueError("Invalid transaction signature")

    # Métodos para obter o fornecimento atual e máximo de tokens
    def get_current_supply(self):
        return self.current_supply

    def get_max_supply(self):
        return self.max_supply