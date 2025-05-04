from utils import to_bytes, from_bytes, BLOCK_SIZE

MIN_DEGREE = 10
MAX_KEYS = 2 * MIN_DEGREE - 1  # 19
MAX_CHILDREN = 2 * MIN_DEGREE  # 20

class Node:
    def __init__(self, block_id, parent_id=0, num_keys=0):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_keys = num_keys
        self.keys = [0] * MAX_KEYS
        self.values = [0] * MAX_KEYS
        self.children = [0] * MAX_CHILDREN

    def to_bytes(self):
        data = bytearray(BLOCK_SIZE)
        data[0:8] = to_bytes(self.block_id)
        data[8:16] = to_bytes(self.parent_id)
        data[16:24] = to_bytes(self.num_keys)

        offset = 24
        for k in self.keys:
            data[offset:offset+8] = to_bytes(k)
            offset += 8
        for v in self.values:
            data[offset:offset+8] = to_bytes(v)
            offset += 8
        for c in self.children:
            data[offset:offset+8] = to_bytes(c)
            offset += 8

        return bytes(data)

    @classmethod
    def from_bytes(cls, data):
        block_id = from_bytes(data[0:8])
        parent_id = from_bytes(data[8:16])
        num_keys = from_bytes(data[16:24])
        offset = 24

        keys = [from_bytes(data[offset + i*8:offset + (i+1)*8]) for i in range(MAX_KEYS)]
        offset += 8 * MAX_KEYS
        values = [from_bytes(data[offset + i*8:offset + (i+1)*8]) for i in range(MAX_KEYS)]
        offset += 8 * MAX_KEYS
        children = [from_bytes(data[offset + i*8:offset + (i+1)*8]) for i in range(MAX_CHILDREN)]

        node = cls(block_id, parent_id, num_keys)
        node.keys = keys
        node.values = values
        node.children = children
        return node
    def is_full(self):
        return self.num_keys >= len(self.keys)

    def insert_into_leaf(self, key, value):
        # Insert key/value into correct position (sorted)
        i = self.num_keys - 1
        while i >= 0 and self.keys[i] > key:
            self.keys[i + 1] = self.keys[i]
            self.values[i + 1] = self.values[i]
            i -= 1
        self.keys[i + 1] = key
        self.values[i + 1] = value
        self.num_keys += 1
    def split(self):
        mid_index = self.num_keys // 2
        mid_key = self.keys[mid_index]
        mid_value = self.values[mid_index]

        left = Node()
        right = Node()
        
        left.num_keys = mid_index
        left.keys[:mid_index] = self.keys[:mid_index]
        left.values[:mid_index] = self.values[:mid_index]

        right.num_keys = self.num_keys - mid_index - 1
        right.keys[:right.num_keys] = self.keys[mid_index + 1:self.num_keys]
        right.values[:right.num_keys] = self.values[mid_index + 1:self.num_keys]

        return mid_key, mid_value, left, right