import ecdsa
import hashlib
import base58
from cryptography.fernet import Fernet
import os

class Wallet:
    def __init__(self, password):
        self.password = password.encode()
        self.key = self.generate_key(self.password)
        self.cipher = Fernet(self.key)
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        self.address = self.generate_address(self.public_key)
        self.balance = 0

    def generate_key(self, password):
        return base58.b58encode(hashlib.sha256(password).digest())

    def generate_private_key(self):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        encrypted_private_key = self.cipher.encrypt(private_key.to_string())
        with open('private_key.enc', 'wb') as f:
            f.write(encrypted_private_key)
        return private_key

    def load_private_key(self):
        with open('private_key.enc', 'rb') as f:
            encrypted_private_key = f.read()
        private_key_bytes = self.cipher.decrypt(encrypted_private_key)
        return ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

    def generate_public_key(self, private_key):
        return private_key.get_verifying_key()

    def generate_address(self, public_key):
        sha256_bpk = hashlib.sha256(public_key.to_string()).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        pre_address = b'\x00' + ripemd160_bpk
        sha256_1 = hashlib.sha256(pre_address).digest()
        sha256_2 = hashlib.sha256(sha256_1).digest()
        checksum = sha256_2[:4]
        binary_address = pre_address + checksum
        address = base58.b58encode(binary_address)
        return address.decode()

    def create_transaction(self, recipient_address, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        transaction = {
            'sender': self.address,
            'recipient': recipient_address,
            'amount': amount
        }
        self.balance -= amount
        return transaction