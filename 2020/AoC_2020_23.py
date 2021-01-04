print("\nPart 1:\n")

# input_string = "389125467"
input_string = "253149867"

print("Input:", input_string, "\n")

init_cups = list(map(int, input_string))
print(init_cups)

def find_dest(max_value, current_cup, picked_cups):
	dest_cup = current_cup - 1
	if dest_cup < 1:
		dest_cup = max_value
	while dest_cup in picked_cups: # this is a do... while, really.
		dest_cup -= 1
		if dest_cup < 1:
			dest_cup = max_value
	return dest_cup

# print(find_dest(max(init_cups), 3, [8, 9, 1]))
# print(find_dest(max(init_cups), 2, [8, 9, 1]))
# print(find_dest(max(init_cups), 5, [4, 6, 7]))

def game(rounds):
	max_value = max(init_cups)
	cups = init_cups[:]
	for i in range(rounds):
		current_cup, picked_cups = cups[0], cups[1 : 4]
		dest_cup = find_dest(max_value, current_cup, picked_cups)
		cups = cups[4 :] + [cups[0]] # removing picked cups, and placing the current at the end.
		index_dest = cups.index(dest_cup)
		cups = cups[: index_dest + 1] + picked_cups + cups[index_dest + 1 :]
	index_next_1 = cups.index(1) + 1
	order = cups[index_next_1 : ] + cups[: index_next_1 - 1]
	return order

def print_sequence(used_fun, rounds):
	order = used_fun(rounds)
	print("\nAfter", rounds, "rounds:", "".join(map(str, order)))

# print_sequence(game, 10)
print_sequence(game, 100)

############################################################
# Circular linked lists:

class Node:

	def __init__(self, value, nextNode = None):
		self.value = value
		self.next = nextNode

class CircularLinkedList:

	def __init__(self):
		self.start = None
		self.end = None
		self.length = 0

	def addLeft(self, value):
		self.start = Node(value, self.start)
		if self.start.next == None:
			self.end = self.start
		self.end.next = self.start
		self.length += 1

	def addRight(self, value):
		if self.end == None:
			self.addLeft(value)
		else:
			self.end.next = Node(value, self.start)
			self.end = self.end.next
			self.length += 1

	def toList(self, startingNode = None):
		if startingNode == None:
			startingNode = self.start
		node = startingNode
		new_list = []
		while node != None:
			new_list.append(node.value)
			node = node.next
			if node == startingNode:
				break
		return new_list

	def find(self, value, startingNode = None):
		if startingNode is None:
			startingNode = self.start
		node = startingNode
		while node != None:
			if node.value == value:
				return node
			node = node.next
			if node == startingNode:
				break
		print("Value", value, "not found.\n")
		return None

	# Careful: both lists are modified!
	def concat(self, otherList):
		if otherList.length == 0:
			return
		elif self.length == 0:
			self.start = otherList.start
		else:
			self.end.next = otherList.start
			otherList.end.next = self.start
		self.end = otherList.end
		self.length += otherList.length

	@staticmethod
	def fromList(regularList):
		cllist = CircularLinkedList()
		for value in regularList:
			cllist.addRight(value)
		return cllist

############################################################
# Testing:

# cllist = CircularLinkedList()
# cllist.addRight(1)
# cllist.addRight(2)
# cllist.addRight(3)
# cllist.addLeft(5)

# cllist2 = CircularLinkedList()
# cllist2.addLeft(0)
# cllist2.addLeft(10)

# print(cllist.toList())
# node = cllist.find(3)
# print(node.next.value) # ok

# print("rotated:", cllist.toList(cllist.start.next)) # wrapping around, from 1st value

# cllist.concat(cllist2)
# print("concat:", cllist.toList())

# cllist3 = CircularLinkedList.fromList(list("hello world"))
# print(cllist3.toList())

############################################################
# Variant using circular linked lists + node hash map:

def get_node_map(cllist):
	node_map = [0] * (cllist.length + 1)
	node = cllist.start
	while node != None:
		node_map[node.value] = node
		node = node.next
		if node == cllist.start:
			break
	return node_map

def game_2(rounds):
	max_value = max(init_cups)
	cups = CircularLinkedList.fromList(init_cups)
	node_map = get_node_map(cups)
	current_cup_node = cups.start

	for i in range(rounds):
		p1 = current_cup_node.next
		p2 = p1.next
		p3 = p2.next

		picked_cups_values = [p1.value, p2.value, p3.value]
		dest_cup_value = find_dest(max_value, current_cup_node.value, picked_cups_values)
		# dest_cup_node = cups.find(dest_cup_value) # terribly slow here!
		dest_cup_node = node_map[dest_cup_value]

		current_cup_node.next = p3.next
		p3.next = dest_cup_node.next
		dest_cup_node.next = p1
		current_cup_node = current_cup_node.next

	cups = cups.toList()
	index_next_1 = cups.index(1) + 1
	order = cups[index_next_1 : ] + cups[: index_next_1 - 1]
	return order

############################################################
# Simpler version: hash map of next indexes!

def game_3(rounds):
	max_value = max(init_cups)
	idx_next_map = [0] * (max_value + 1)
	for i in range(len(init_cups)):
		idx_next_map[init_cups[i]] = init_cups[(i + 1) % len(init_cups)]

	current_index = init_cups[0]
	for i in range(rounds):
		p1 = idx_next_map[current_index]
		p2 = idx_next_map[p1]
		p3 = idx_next_map[p2]

		dest_cup_value = find_dest(max_value, current_index, [p1, p2, p3])

		idx_next_map[current_index] = idx_next_map[p3]
		idx_next_map[p3] = idx_next_map[dest_cup_value]
		idx_next_map[dest_cup_value] = p1
		current_index = idx_next_map[current_index]

	current_index, order = idx_next_map[1], []
	while current_index != 1:
		order += [current_index]
		current_index = idx_next_map[current_index]
	return order

############################################################

print("\nPart 2:\n")

def get_mult(used_fun, rounds):
	order = used_fun(rounds)
	print("\nResult:", order[0] * order[1])

bound = 1000000
rounds = 10000000

init_cups += range(max(init_cups) + 1, bound + 1)

# # get_mult(game, rounds) # terribly slow!
# get_mult(game_2, rounds)
get_mult(game_3, rounds) # fast!
