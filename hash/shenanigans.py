# to sa moje glupoty nie patrz na to wgl pls


from binary_tree import BalancedBinaryTree as BBT
from hash_table import HashTable as HT

k = 10
n = 1000

hashTable = HT(k)

for x in range(n):
	hashTable.add(x.__str__())
	print(len(hashTable))
	# print(x, " ", hashTable.calculate_hash(x.__str__()))

xd = 5

for i in range(xd):
	hashTable.add("0")

print(hashTable)


for x in range(n):
	hashTable.remove(x.__str__())
	print(len(hashTable))
	# print(x, " ", hashTable.calculate_hash(x.__str__()))

print(hashTable)

for i in range(xd):
	hashTable.remove("0")
	# print(len(hashTable.table[0]))
	print(len(hashTable))
# hashTable.remove("0")
#
# print(hashTable)
