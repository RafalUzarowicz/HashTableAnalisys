# to sa moje glupoty nie patrz na to wgl pls
import random

from binary_tree import BalancedBinaryTree as BBT
from hash_table import HashTable as HT

k = 2
n = 100
hashTable = HT(k)

for x in range(n):
	i = random.randint(0, 10)
	hashTable.add(i.__str__())
	# print(len(hashTable))
	# print(x, " ", hashTable.calculate_hash(x.__str__()))

xd = 50000

for i in range(xd):
	hashTable.add("")

# for tree in hashTable:
# 	for node in tree:
# 		print(node)

# for elem in hashTable:
# 	print(elem)

print(hashTable)


for x in range(n):
	hashTable.remove(x.__str__())
	# print(len(hashTable))
	# print(x, " ", hashTable.calculate_hash(x.__str__()))

# print(hashTable)

for i in range(xd):
	hashTable.remove("")
	# print(len(hashTable.table[0]))
	# print(len(hashTable))
# hashTable.remove("0")
#
# print(hashTable)
