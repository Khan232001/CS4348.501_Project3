from utils import to_bytes, from_bytes, BLOCK_SIZE

MAX_KEYS = 19
MAX_CHILDREN = MAX_KEYS + 1

class Node:
    def __init__(self, block_id, is_leaf=True, parent_id=0):
        self.block_id = block_id
        self.is_leaf = is_leaf
        self.parent_id = parent_id
        self.num_keys = 0
        self.keys = [0] * MAX_KEYS
        self.values = [''] * MAX_KEYS
        self.children = [0] * MAX_CHILDREN

    def is_full(self):
        return self.num_keys >= MAX_KEYS

    def insert_into_leaf(self, key, value):
        idx = 0
        while idx < self.num_keys and self.keys[idx] < key:
            idx += 1

        # Shift keys/values to make space
        for i in range(self.num_keys, idx, -1):
            self.keys[i] = self.keys[i-1]
            self.values[i] = self.values[i-1]

        self.keys[idx] = key
        self.values[idx] = value
        self.num_keys += 1

    def to_bytes(self):
        b = bytearray(BLOCK_SIZE)

        b[0] = int(self.is_leaf)
        b[1:9] = to_bytes(self.parent_id)
        b[9:17] = to_bytes(self.num_keys)

        offset = 17

        # Keys (19 * 8 bytes)
        for i in range(MAX_KEYS):
            b[offset:offset+8] = to_bytes(self.keys[i])
            offset += 8

        # Values (19 * 8 bytes → use fixed 8-char strings)
        for i in range(MAX_KEYS):
            val_bytes = self.values[i].encode('utf-8')[:8]
            val_bytes = val_bytes.ljust(8, b'\x00')
            b[offset:offset+8] = val_bytes
            offset += 8

        # Children (20 * 8 bytes)
        for i in range(MAX_CHILDREN):
            b[offset:offset+8] = to_bytes(self.children[i])
            offset += 8

        return bytes(b)

    @staticmethod
    def from_bytes(data):
        is_leaf = bool(data[0])
        parent_id = from_bytes(data[1:9])
        num_keys = from_bytes(data[9:17])
        offset = 17

        keys = []
        for _ in range(MAX_KEYS):
            keys.append(from_bytes(data[offset:offset+8]))
            offset += 8

        values = []
        for _ in range(MAX_KEYS):
            val = data[offset:offset+8].rstrip(b'\x00').decode('utf-8')
            values.append(val)
            offset += 8

        children = []
        for _ in range(MAX_CHILDREN):
            children.append(from_bytes(data[offset:offset+8]))
            offset += 8

        node = Node(block_id=0, is_leaf=is_leaf, parent_id=parent_id)
        node.keys = keys
        node.values = values
        node.children = children
        node.num_keys = num_keys

        return node