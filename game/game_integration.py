class GameIntegration:
    def __init__(self, blockchain, wallet):
        self.blockchain = blockchain
        self.wallet = wallet

    def reward_player(self, player_id, amount):
        self.wallet.add_funds(amount)
        self.blockchain.add_block(f"Rewarded player {player_id} with {amount} coins")