# Classless variant, using global vars. FASTER!
# Be careful, not using the 'global' keyword may break the whole thing!

print("\nPart 1:\n")

init_size = 10000 # arbitrary
hash_map = [(0, 0, 0)]
current_epoch = 0
last_value = 0

def initGame(starting_list):
	global hash_map
	global current_epoch
	hash_map = [(0, 0, 0)] * init_size # hash_map: key -> (count, age1, age2)
	current_epoch = 1
	n = len(starting_list)
	for i in range(n):
		add(starting_list[i])

def printGame():
	print("hash_map:", hash_map[0 : 100]) # 100 first values
	print("current_epoch:", current_epoch)
	print("last_value:", last_value)

def add(value):
	global hash_map
	global current_epoch
	global last_value
	while value >= len(hash_map):
		hash_map.extend([(0, 0, 0)] * len(hash_map)) # doubling the size!
	count, age1, age2 = hash_map[value]
	hash_map[value] = (count + 1, age2, current_epoch)
	current_epoch += 1
	last_value = value

def next():
	count, age1, age2 = hash_map[last_value]
	if count == 1:
		new_value = 0
	else:
		new_value = age2 - age1
	# print("epoch:", current_epoch, "choosing:", new_value)
	add(new_value)
	return new_value

def find_nth(nth, starting_list):
	initGame(starting_list)
	for i in range(nth - len(starting_list)):
		next()
	result = last_value
	print(result)
	return result

result = find_nth(2020, [0, 13, 1, 8, 6, 15])


print("\nPart 2:\n")

result = find_nth(30000000, [0, 13, 1, 8, 6, 15]) # ~ 21 sec
