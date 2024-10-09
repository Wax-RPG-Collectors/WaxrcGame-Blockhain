import unittest
from blockchain.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def test_genesis_block(self):
        blockchain = Blockchain()
        self.assertEqual(blockchain.chain[0].data, "Genesis Block")

    def test_add_block(self):
        blockchain = Blockchain()
        blockchain.add_block("Test Block")
        self.assertEqual(blockchain.chain[-1].data, "Test Block")