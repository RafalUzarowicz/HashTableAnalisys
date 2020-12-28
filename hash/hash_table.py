import hashlib

from binary_tree import BalancedBinaryTree as AVL

"""
    Author: Rafał Uzarowicz - https://github.com/RafalUzarowicz
"""


class HashTable:
	def __init__(self, length: int):
		self.k = length
		self.table = [None] * self.k

	def add(self, value: str):
		key = self.__calculate_hash(value)
		if self.table[key] is None:
			self.table[key] = AVL()
		else:
			self.table[key].insert(value)

	def remove(self, value: str):
		key = self.__calculate_hash(value)
		if self.table[key] is not None:
			self.table[key].delete(value)

	def __getitem__(self, item: int):
		# TODO: opis co zwraca funkcja itp
		return self.table[item]

	def __calculate_hash(self, value: str) -> int:
		return int(hashlib.md5(value.encode()).hexdigest(), 16) % self.k
