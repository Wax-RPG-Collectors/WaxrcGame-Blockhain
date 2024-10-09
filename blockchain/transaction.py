import hashlib

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def calculate_hash(self):
        transaction_string = f"{self.sender}{self.recipient}{self.amount}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def sign_transaction(self, signing_key):
        if signing_key.get_verifying_key().to_string().hex() != self.sender:
            raise ValueError("You cannot sign transactions for other wallets!")
        self.signature = signing_key.sign(self.calculate_hash().encode())

    def is_valid(self):
        if self.sender == "0":  # Assuming "0" is the address for mining rewards
            return True
        if not self.signature:
            raise ValueError("No signature in this transaction")
        public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1)
        return public_key.verify(self.signature, self.calculate_hash().encode())