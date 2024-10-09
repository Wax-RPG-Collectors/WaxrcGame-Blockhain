import unittest
from wallet.wallet import Wallet

class TestWallet(unittest.TestCase):
    def test_initial_balance(self):
        wallet = Wallet()
        self.assertEqual(wallet.balance, 0)

    def test_add_funds(self):
        wallet = Wallet()
        wallet.add_funds(100)
        self.assertEqual(wallet.balance, 100)

    def test_spend_funds(self):
        wallet = Wallet()
        wallet.add_funds(100)
        result = wallet.spend_funds(50)
        self.assertTrue(result)
        self.assertEqual(wallet.balance, 50)