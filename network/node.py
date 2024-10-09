import requests

class Node:
    def __init__(self, address):
        self.address = address
        self.peers = []

    def add_peer(self, peer_address):
        if peer_address not in self.peers:
            self.peers.append(peer_address)

    def get_peers(self):
        return self.peers

    def broadcast_new_block(self, block):
        for peer in self.peers:
            try:
                response = requests.post(f"http://{peer}/rpc", json={
                    'method': 'add_block',
                    'params': [block.__dict__]
                })
                if response.status_code != 200:
                    print(f"Failed to notify peer {peer}")
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to peer {peer}: {e}")

    def request_chain(self):
        for peer in self.peers:
            try:
                response = requests.post(f"http://{peer}/rpc", json={
                    'method': 'get_blockchain',
                    'params': []
                })
                if response.status_code == 200:
                    return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to peer {peer}: {e}")
        return None