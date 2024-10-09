from flask import Flask, request, jsonify
from config import Config  # Ensure Config is imported
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet

app = Flask(__name__)

blockchain = Blockchain()
wallet = Wallet()

@app.route('/rpc', methods=['POST'])
def rpc():
    data = request.get_json()
    method = data.get('method')
    params = data.get('params', [])

    if method == 'get_blockchain':
        return jsonify([block.__dict__ for block in blockchain.chain])
    elif method == 'generate_block':
        if len(params) != 1:
            return jsonify({'error': 'Invalid parameters'}), 400
        block_data = params[0]
        blockchain.generate_block(block_data)
        return jsonify({'message': 'Block generated'})
    elif method == 'get_balance':
        return jsonify({'balance': wallet.balance})
    elif method == 'create_transaction':
        if len(params) != 3:
            return jsonify({'error': 'Invalid parameters'}), 400
        sender, recipient, amount = params
        try:
            transaction_hash = blockchain.create_transaction(sender, recipient, amount)
            return jsonify({'transaction_hash': transaction_hash})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    elif method == 'add_node':
        if len(params) != 1:
            return jsonify({'error': 'Invalid parameters'}), 400
        blockchain.add_node(params[0])
        return jsonify({'message': 'Node added'})
    elif method == 'get_nodes':
        return jsonify({'nodes': blockchain.get_nodes()})
    elif method == 'synchronize':
        blockchain.synchronize()
        return jsonify({'message': 'Blockchain synchronized'})
    elif method == 'generate_addresses':
        if len(params) != 2:
            return jsonify({'error': 'Invalid parameters'}), 400
        private_key_hex, count = params
        addresses = wallet.generate_addresses_from_private_key(private_key_hex, count)
        return jsonify({'addresses': addresses})
    elif method == 'create_token':
        if len(params) != 4:
            return jsonify({'error': 'Invalid parameters'}), 400
        name, symbol, initial_supply, decimals = params
        try:
            blockchain.create_token(name, symbol, initial_supply, decimals)
            return jsonify({'message': 'Token created'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    elif method == 'get_token_balance':
        if len(params) != 2:
            return jsonify({'error': 'Invalid parameters'}), 400
        symbol, address = params
        try:
            balance = blockchain.get_token_balance(symbol, address)
            return jsonify({'balance': balance})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    elif method == 'transfer_token':
        if len(params) != 4:
            return jsonify({'error': 'Invalid parameters'}), 400
        symbol, from_address, to_address, amount = params
        try:
            blockchain.transfer_token(symbol, from_address, to_address, amount)
            return jsonify({'message': 'Token transferred'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    elif method == 'mine_pending_transactions':
        if len(params) != 1:
            return jsonify({'error': 'Invalid parameters'}), 400
        miner_address = params[0]
        try:
            new_block = blockchain.mine_pending_transactions(miner_address)
            if new_block:
                return jsonify({'message': 'New block mined', 'block': new_block.__dict__})
            else:
                return jsonify({'message': 'No transactions to mine'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    elif method == 'confirm_transaction':
        if len(params) != 1:
            return jsonify({'error': 'Invalid parameters'}), 400
        transaction_hash = params[0]
        try:
            confirmed = blockchain.confirm_transaction(transaction_hash)
            return jsonify({'confirmed': confirmed})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    elif method == 'get_current_supply':
        return jsonify({'current_supply': blockchain.get_current_supply()})
    elif method == 'get_max_supply':
        return jsonify({'max_supply': blockchain.get_max_supply()})
    elif method == 'calculate_transaction_fee':
        if len(params) != 2:
            return jsonify({'error': 'Invalid parameters'}), 400
        amount, fast = params
        fee = blockchain.calculate_transaction_fee(amount, fast)
        return jsonify({'transaction_fee': fee})
    elif method == 'calculate_token_creation_fee':
        fee = blockchain.calculate_token_creation_fee()
        return jsonify({'token_creation_fee': fee})
    elif method == 'calculate_game_creation_fee':
        fee = blockchain.calculate_game_creation_fee()
        return jsonify({'game_creation_fee': fee})
    elif method == 'sign_transaction':
        if len(params) != 2:
            return jsonify({'error': 'Invalid parameters'}), 400
        transaction, private_key = params
        signed_transaction = blockchain.sign_transaction(transaction, private_key)
        return jsonify({'signed_transaction': signed_transaction})
    elif method == 'verify_transaction_signature':
        if len(params) != 1:
            return jsonify({'error': 'Invalid parameters'}), 400
        transaction = params[0]
        valid = blockchain.verify_transaction_signature(transaction)
        return jsonify({'valid': valid})
    elif method == 'add_transaction':
        if len(params) != 2:
            return jsonify({'error': 'Invalid parameters'}), 400
        transaction, private_key = params
        try:
            blockchain.add_transaction(transaction, private_key)
            return jsonify({'message': 'Transaction added'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Method not found'}), 404

if __name__ == '__main__':
    app.run(port=Config.RPC_PORT)