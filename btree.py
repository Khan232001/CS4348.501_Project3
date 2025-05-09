class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

    def is_full(self):
        return len(self.keys) == 2 * self.t - 1

    def traverse(self):
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].traverse()
            print(f"{self.keys[i]} : {self.values[i]}")
        if not self.leaf:
            self.children[-1].traverse()

    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and self.keys[i] == key:
            return self.values[i]
        if self.leaf:
            return None
        return self.children[i].search(key)

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def search(self, key):
        return self.root.search(key)

    def insert(self, key, value):
        # Prevent duplicate keys
        if self.search(key) is not None:
            print(f"Error: Duplicate key {key} not allowed.")
            return

        root = self.root
        if root.is_full():
            s = BTreeNode(self.t, False)
            s.children.insert(0, root)
            self._split_child(s, 0)
            self._insert_non_full(s, key, value)
            self.root = s
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            # Prevent duplicate keys in leaf nodes
            if key in node.keys:
                print(f"Error: Duplicate key {key} not allowed.")
                return
            
            node.keys.append(0)
            node.values.append(0)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if node.children[i].is_full():
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, i):
        t = self.t
        y = parent.children[i]
        z = BTreeNode(t, y.leaf)

        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])
        parent.values.insert(i, y.values[t - 1])

        z.keys = y.keys[t:]
        z.values = y.values[t:]
        y.keys = y.keys[:t - 1]
        y.values = y.values[:t - 1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

    def print_tree(self):
        self.root.traverse()

    def inorder_items(self):
        items = []

        def _traverse(node):
            for i in range(len(node.keys)):
                if not node.leaf:
                    _traverse(node.children[i])
                items.append((node.keys[i], node.values[i]))
            if not node.leaf:
                _traverse(node.children[-1])

        _traverse(self.root)
        return items
