from hashlib import md5

from binary_tree import BalancedBinaryTree as Tree

"""
    Author: Rafał Uzarowicz - https://github.com/RafalUzarowicz
"""


class HashTable:
	class HashTableIterator:
		def __init__(self, table):
			self._table = table
			self._element_index = 0
			self._table_index = 0
			self._iterator = None

		def __find_next(self, starting_index):
			index = starting_index
			while index < self._table.k and self._table[index] is None:
				index = index + 1
			self._table_index = index

		def __next__(self):
			if self._table_index < self._table.k and self._element_index < len(self._table):
				if self._iterator is None:
					self._iterator = iter(self._table[self._table_index])
				try:
					return next(self._iterator).value
				except StopIteration:
					self.__find_next(self._table_index + 1)
					if self._table_index < self._table.k:
						self._iterator = iter(self._table[self._table_index])
						return next(self._iterator).value
			raise StopIteration

	def __init__(self, length: int):
		self.k = length
		self.table = [None] * self.k
		self._size = 0

	def __iter__(self):
		return self.HashTableIterator(self)

	def __len__(self):
		return self._size

	def add(self, value: str):
		key = self.__calculate_hash(value)
		if self.table[key] is None:
			self.table[key] = Tree()
		self.table[key].insert(value)
		self._size = self._size + 1

	def remove(self, value: str):
		key = self.__calculate_hash(value)
		if self.table[key] is not None:
			tree_size = len(self.table[key])
			self.table[key].delete(value)
			if tree_size > len(self.table[key]):
				self._size = self._size - 1

	def __getitem__(self, item):
		return self.table[item]

	def __calculate_hash(self, value: str) -> int:
		return int(md5(value.encode()).hexdigest(), 16) % self.k

