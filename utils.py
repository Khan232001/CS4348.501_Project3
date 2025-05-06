import csv

# Constants
MAGIC = b"4348PRJ3"  # ✅ Correct magic number as per project spec
BLOCK_SIZE = 4096    # Each block in the index file is 4096 bytes

# Helper functions for encoding/decoding integers
def to_bytes(value, length=8):
    return value.to_bytes(length, byteorder='big')

def from_bytes(data):
    return int.from_bytes(data, byteorder='big')

# Load key/value pairs from a text file
def load_data_from_file(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                key, value = parts
                data.append((int(key), value))
    return data

# Write all key/value pairs to a CSV file
def write_output_to_csv(tree):
    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Key", "Value"])
        for key, value in tree.inorder_items():
            writer.writerow([key, value])