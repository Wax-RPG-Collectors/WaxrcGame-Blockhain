import unittest
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
from game.game_integration import GameIntegration

class TestGameIntegration(unittest.TestCase):
    def test_reward_player(self):
        blockchain = Blockchain()
        wallet = Wallet()
        game_integration = GameIntegration(blockchain, wallet)
        
        game_integration.reward_player("player1", 100)
        self.assertEqual(wallet.balance, 100)
        self.assertEqual(blockchain.chain[-1].data, "Rewarded player player1 with 100 coins")