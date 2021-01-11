# to sa moje glupoty nie patrz na to wgl pls


from binary_tree import BalancedBinaryTree as BBT
from hash_table import HashTable as HT


hashTable = HT(2)

for x in range(10):
	hashTable.add(x.__str__())
	# print(x, " ", hashTable.calculate_hash(x.__str__()))

hashTable.add("0")
hashTable.add("0")
hashTable.add("0")
hashTable.add("0")

print(hashTable)

hashTable.remove("0")
hashTable.remove("0")
hashTable.remove("0")
hashTable.remove("0")
hashTable.remove("0")
hashTable.remove("0")

print(hashTable)
