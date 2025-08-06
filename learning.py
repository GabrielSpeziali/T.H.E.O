import json
import sys
from collections import defaultdict

sys.path.append(r"F:\python_libs")

class Memory:
    def __init__(self, file='memory.json'):
        self.file = file
        self.data = defaultdict(int)
        self.load()

    def load(self):
        try:
            with open(self.file, 'r') as f:
                self.data.update(json.load(f))
        except FileNotFoundError:
            pass

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def remember_command(self, cmd):
        self.data[cmd] += 1
        self.save()

    def most_used(self, top=3):
        return sorted(self.data.items(), key=lambda x: x[1], reverse=True)[:top]
