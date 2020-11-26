"""
    Author: Rafał Uzarowicz - https://github.com/RafalUzarowicz
"""


class BinaryTree:
    class Node:
        def __init__(self, value: str):
            self.value = value
            self.parent = None
            self.height = 1
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, value: str):
        # TODO: dodawanie do drzewa
        # TODO: balansowanie drzewa
        def binary_insert(node: BinaryTree.Node):
            pass

        binary_insert(self.root)

    def delete(self, value: str):
        # TODO: usuwanie z drzewa
        # TODO: balansowanie drzewa
        def binary_delete(node: BinaryTree.Node):
            pass

        binary_delete(self.root)
