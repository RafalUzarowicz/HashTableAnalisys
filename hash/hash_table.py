from hashlib import md5

from hash.binary_tree import BalancedBinaryTree as Tree

"""
	projekt: Analiza tablicy mieszającej (warianty W13 i W21)
	autor: Rafał Uzarowicz - https://github.com/RafalUzarowicz
"""


class HashTable:
	def __init__(self, length: int):
		if not isinstance(length, int) or length <= 0:
			raise ValueError("Table size should be positive number.")
		self.k = length
		self.table = [None] * self.k
		self._size = 0

	def __iter__(self):
		for tree in self.table:
			if tree is not None:
				for node in tree:
					yield node

	def __len__(self):
		return self._size

	def add(self, value: str) -> None:
		key = self.calculate_hash(value)
		if self.table[key] is None:
			self.table[key] = Tree()
		self.table[key].insert(value)
		self._size = self._size + 1

	def remove(self, value: str) -> None:
		key = self.calculate_hash(value)
		if self.table[key] is not None:
			tree_size = len(self.table[key])
			self.table[key].delete(value)
			if tree_size > len(self.table[key]):
				self._size = self._size - 1

	def __getitem__(self, item):
		return self.table[item]

	def __str__(self):
		string = ""
		for i in range(self.k):
			string += str(i)+":\n"
			string += str(self.table[i])
			string += "\n"
		return string

	def calculate_hash(self, value: str) -> int:
		return int(md5(value.encode()).hexdigest(), 16) % self.k

