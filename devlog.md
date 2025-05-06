## 2025-04-30 20:00

**Thoughts So Far:**
This is the start of Project 3. I'm building a command-line B-Tree index file manager in Python. The file structure is 512-byte blocks, with a header and nodes stored directly to disk. Python makes it easier to handle big-endian encoding.

**Plan:**
- Set up the CLI to handle the `create` command.
- Write the first block (header) with the correct format:
  - Magic number: "4348PRJ3"
  - Root ID: 0 (empty tree)
  - Next block ID: 1 (root would go here)
- Ensure the file fails to create if it already exists.

**End of Session Reflection:**
The `create` command is working. It writes a proper 512-byte header with the correct layout. I’ve included error handling for invalid arguments and existing files. Tomorrow, I’ll start working on the `insert` logic and block node layout.

---

## 2025-05-01 20:00

**Thoughts So Far:**
Yesterday I implemented the `create` command and set up the header format. Today I needed to start handling node structures and insertions. The tree is disk-based, so I had to serialize and deserialize each node manually. Python’s `bytearray` came in handy here.

**Plan:**
- Define a `Node` class to match the B-Tree structure (with 19 key/value pairs and 20 children).
- Add methods to convert `Node` objects to/from 512-byte blocks.
- Implement `insert` in `btree.py` to insert into an empty tree and create the root node.
- Update the header to track the new root and next available block ID.

**Problems & Fixes:**
- I got a `TypeError` when modifying the header block — turns out `bytes` is immutable in Python. I fixed this by converting it to `bytearray` before modifying.

**End of Session Reflection:**
The `insert` command now successfully adds a key/value pair to an empty tree and updates the root. I confirmed it writes the root node to block 1 and sets up the next available block as 2. Tomorrow, I’ll start implementing insertion into existing nodes and consider handling node splits when full.
## 2025-05-02 20:00

**Thoughts So Far:**
The B-Tree now supports inserting into an empty tree. Today’s goal is to support multiple insertions into the root node and reject inserts when the node is full. I’m assuming the root has room and focusing on correct insertion logic in sorted order.

**Plan:**
- Read the root node from disk
- If the node has space, insert the new key/value in sorted order
- If it’s full, print a message (splitting will be handled tomorrow)
- Update the node on disk after insertion

**End of Session Reflection:**
I successfully inserted multiple key/value pairs into the root node, preserving sorted order. The insert function reads the root, updates it in memory, and writes it back to disk. Tomorrow I’ll add node-splitting logic.

## 2025-05-03 17:45

**Thoughts So Far:**
The tree now allows inserting into a single leaf node, but we need true B-Tree behavior: splitting full nodes and managing multiple levels. I’ll implement root splitting today, followed by recursive splits in child nodes.

**Plan:**
- Detect when the root is full
- Allocate two new child nodes from the root’s contents
- Promote the middle key to a new root
- Adjust `insert()` to allow recursive insert into children

**End of Session Reflection:**
Root node splitting works! The tree now supports a second level. This required adjusting insert logic, maintaining sorted keys, and correctly writing nodes to disk. I’ve laid the foundation for recursive insertion into child nodes, which comes next.


## 2025-05-06 17:25
- Verified complete insert logic for basic B+ tree functionality.
- Cleaned up code and added documentation.
- Prepared project for final submission and testing.


