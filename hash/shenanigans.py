# to sa moje glupoty nie patrz na to wgl pls


from binary_tree import BalancedBinaryTree as BBT
from hash_table import HashTable as HT

k = 5
n = 10

hashTable = HT(k)

for x in range(n):
	hashTable.add(x.__str__())
	# print(len(hashTable))
	# print(x, " ", hashTable.calculate_hash(x.__str__()))

xd = 5

for i in range(xd):
	hashTable.add("0")

# for tree in hashTable:
# 	for node in tree:
# 		print(node)

for elem in hashTable:
	print(elem)

print(hashTable)


for x in range(n):
	hashTable.remove(x.__str__())
	# print(len(hashTable))
	# print(x, " ", hashTable.calculate_hash(x.__str__()))

# print(hashTable)

for i in range(xd):
	hashTable.remove("0")
	# print(len(hashTable.table[0]))
	print(len(hashTable))
# hashTable.remove("0")
#
# print(hashTable)
