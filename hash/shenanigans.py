# to sa moje glupoty nie patrz na to wgl pls


from binary_tree import BalancedBinaryTree as BBT
from hash_table import HashTable as HT


hashTable = HT(5)

for x in range(10):
	hashTable.add(x.__str__())
	print(x, " ", hashTable.calculate_hash(x.__str__()))

for x in hashTable.table:
	print(x)
	print("---------------------------")