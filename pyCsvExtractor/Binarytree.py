class Binarytree:
    def __init__(self):
        self.left = None
        self.right = None
        self.val = None

    def setVal(self, val):
        self.val = val

    # A utility function to insert
    # a new node with the given key
    def insert(self, key):
        if self.val is None:
            self.val = key
        if self.val < key:
            if self.right is None:
                self.right = Binarytree()
            self.right.insert(key)
        if self.val > key:
            if self.left is None:
                self.left = Binarytree()
            self.left.insert(key)

    def shear(self, key: int) -> bool:
        if self.val is None:
            return False
        if self.val == key:
            return True
        if self.val < key:
            return self.right is not None and self.right.shear(key)
        if self.val > key:
            return self.left is not None and  self.left.shear(key)
t = Binarytree()
t.insert(5)
t.insert(8)
t.insert(1)
print(t.shear(1))
