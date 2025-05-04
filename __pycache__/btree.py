import os
from utils import to_bytes, from_bytes, MAGIC, BLOCK_SIZE
from node import Node

class IndexFile:
    def __init__(self, filename):
        self.filename = filename

    def create(self):
        if os.path.exists(self.filename):
            print(f"Error: File '{self.filename}' already exists.")
            exit(1)

        with open(self.filename, 'wb') as f:
            header = bytearray(BLOCK_SIZE)
            header[0:8] = MAGIC
            header[8:16] = to_bytes(0)   # Root block ID
            header[16:24] = to_bytes(1)  # Next available block ID
            f.write(header)
            print(f"Created index file '{self.filename}'")

    def insert(self, key, value):
        with open(self.filename, 'r+b') as f:
            f.seek(0)
            header = bytearray(f.read(BLOCK_SIZE))  # mutable
            root_id = from_bytes(header[8:16])
            next_block_id = from_bytes(header[16:24])

            if root_id == 0:
                # Tree is empty – create new root node
                node = Node(block_id=1)
                node.keys[0] = key
                node.values[0] = value
                node.num_keys = 1

                f.seek(BLOCK_SIZE)  # Block 1
                f.write(node.to_bytes())

                # Update header
                header[8:16] = to_bytes(1)   # Set root ID to 1
                header[16:24] = to_bytes(2)  # Next block will be 2
                f.seek(0)
                f.write(header)

                print(f"Inserted ({key}, {value}) into new root")
            else:
                root_offset = root_id * BLOCK_SIZE
                f.seek(root_offset)
                root_data = f.read(BLOCK_SIZE)
                root = Node.from_bytes(root_data)

                if root.is_full():
                    print("Root node is full. Splitting...")

                    mid_key, mid_val, left, right = root.split()

                    # Write left node
                    left.block_id = next_block_id
                    f.seek(left.block_id * BLOCK_SIZE)
                    f.write(left.to_bytes())

                    # Write right node
                    right.block_id = next_block_id + 1
                    f.seek(right.block_id * BLOCK_SIZE)
                    f.write(right.to_bytes())

                    # Create new root node
                    new_root = Node(block_id=next_block_id + 2)
                    new_root.keys[0] = mid_key
                    new_root.values[0] = mid_val
                    new_root.num_keys = 1
                    # Future update: set child pointers
                    f.seek(new_root.block_id * BLOCK_SIZE)
                    f.write(new_root.to_bytes())

                    # Update header
                    header[8:16] = to_bytes(new_root.block_id)  # New root ID
                    header[16:24] = to_bytes(next_block_id + 3)  # Next block ID
                    f.seek(0)
                    f.write(header)

                    print(f"Split root. New root ID: {new_root.block_id}")

                else:
                    root.insert_into_leaf(key, value)
                    f.seek(root_offset)
                    f.write(root.to_bytes())
                    print(f"Inserted ({key}, {value}) into root node")