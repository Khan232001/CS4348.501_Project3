def to_bytes(n):
    return n.to_bytes(8, byteorder='big')

def from_bytes(b):
    return int.from_bytes(b, byteorder='big')

MAGIC = b'4348PRJ3'  # 8 bytes
BLOCK_SIZE = 512