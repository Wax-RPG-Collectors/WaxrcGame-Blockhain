import os
import json

class BatchStorage:
    def __init__(self, directory='batches'):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_batch(self, blocks, batch_number):
        batch_file = os.path.join(self.directory, f'batch_{batch_number}.json')
        with open(batch_file, 'w') as f:
            json.dump([block.__dict__ for block in blocks], f)

    def load_batches(self):
        batches = []
        for filename in sorted(os.listdir(self.directory)):
            if filename.startswith('batch_') and filename.endswith('.json'):
                with open(os.path.join(self.directory, filename), 'r') as f:
                    batch = json.load(f)
                    batches.extend(batch)
        return batches