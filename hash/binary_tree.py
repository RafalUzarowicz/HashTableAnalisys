"""
    Author: Rafał Uzarowicz - https://github.com/RafalUzarowicz
"""


class BalancedBinaryTree:
	class TreeIterator:
		def __init__(self, tree):
			self._stack = []
			self.__prepare_stack(tree.root)

		def __prepare_stack(self, node):
			temp_node = node
			while temp_node is not None:
				self._stack.append(temp_node)
				temp_node = temp_node.left

		def __next__(self):
			if len(self._stack) > 0:
				node = self._stack.pop()
				self.__prepare_stack(node.right)
				return node
			raise StopIteration

	class Node:
		def __init__(self, value: str):
			self.value = value
			self.height = 1
			self.left = None
			self.right = None
			self.parent = None

	def __init__(self):
		self.root = None
		self.size = 0

	def __iter__(self):
		return BalancedBinaryTree.TreeIterator(self)

	def insert(self, value: str):
		self.root = self.__avl_insert(self.root, value)

	def __avl_insert(self, root: Node, value: str):
		# Insertion
		if root is None:
			root = self.Node(value)
			self.size = self.size + 1
		elif value < root.value:
			root.left = self.__avl_insert(root.left, value)
			root.left.parent = root
		else:
			root.right = self.__avl_insert(root.right, value)
			root.right.parent = root

		# Balancing
		self.__update_height(root)
		balance = self.__get_balance(root)

		if balance > 1:
			if value < root.left.value:
				return self.__right(root)
			else:
				return self.__left_right(root)
		if balance < -1:
			if value > root.right.value:
				return self.__left(root)
			else:
				return self.__right_left(root)

		return root

	def __get_height(self, node: Node) -> int:
		if node is None:
			return 0
		else:
			return node.height

	def __get_balance(self, node: Node) -> int:
		if node is None:
			return 0
		else:
			return self.__get_height(node.left) - self.__get_height(node.right)

	def delete(self, value: str):
		self.root = self.__avl_delete(self.root, value)

	def __avl_delete(self, root: Node, value: str):

		# Deletion
		if root is None:
			return root
		elif value < root.value:
			root.left = self.__avl_delete(root.left, value)
		elif value > root.value:
			root.right = self.__avl_delete(root.right, value)
		else:
			if root.left is None:
				temp_node = root.right
				return temp_node
			elif root.right is None:
				temp_node = root.left
				return temp_node
			temp_node = self.__get_next_minimal(root.right)
			root.value = temp_node.value
			root.right = self.__avl_delete(root.right, temp_node.value)
			self.size = self.size - 1

		# Balancing

		self.__update_height(root)
		balance = self.__get_balance(root)

		if balance > 1:
			if self.__get_balance(root.left) >= 0:
				return self.__right(root)
			else:
				return self.__left_right(root)
		if balance < -1:
			if self.__get_balance(root) <= 0:
				return self.__left(root)
			else:
				return self.__right_left(root)
		return root

	def __get_next_minimal(self, node: Node) -> Node:
		if node is None or node.left is None:
			return node
		else:
			return self.__get_next_minimal(node.left)

	def __left(self, node: Node) -> Node:
		right_node = node.right
		if right_node is not None:
			node.right = right_node.left
			right_node.left = node
			right_node.parent = node.parent
			node.parent = right_node
			self.__update_height(node)
			self.__update_height(right_node)
			return right_node
		else:
			raise ValueError("There is no child node to rotate.")

	def __right(self, node: Node) -> Node:
		left_node = node.left
		if left_node is not None:
			node.left = left_node.right
			left_node.right = node
			left_node.parent = node.parent
			node.parent = left_node
			self.__update_height(node)
			self.__update_height(left_node)
			return left_node
		else:
			raise ValueError("There is no child node to rotate.")

	def __update_height(self, node: Node):
		node.height = 1 + max(self.__get_height(node.left), self.__get_height(node.right))

	def __left_right(self, node: Node) -> Node:
		if node.left is not None:
			node.left = self.__left(node.left)
			return self.__right(node)
		else:
			raise ValueError("There is no child node to rotate.")

	def __right_left(self, node: Node) -> Node:
		if node.right is not None:
			node.right = self.__right(node.right)
			return self.__left(node)
		else:
			raise ValueError("There is no child node to rotate.")

	def print_tree(self):
		self.__print_tree(self.root, "", True)

	def __print_tree(self, node: Node, indent, last):
		if node is not None:
			print(indent, end='')
			if last:
				print("\____", end='')
				indent += "     "
			else:
				print("\____", end='')
				indent += "|    "
			print(node.value)
			self.__print_tree(node.left, indent, False)
			self.__print_tree(node.right, indent, True)


tree = BalancedBinaryTree()
nums = ["33", "13", "52", "9", "21", "61", "8", "11"]
for num in nums:
	tree.insert(num)

for num in tree:
	print(num.value)
