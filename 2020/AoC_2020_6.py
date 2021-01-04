print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

filename = "resources/example_6"
lines = get_lines(filename)


def count_answsers_1(declaration_map):
	count = 0
	for i in range(0, len(declaration_map)):
		if declaration_map[i] > 0:
			count += 1
	return count

def find_1(lines):
	count = 0
	declaration_map = [0] * 26 # a to z
	for line in lines:
		if line == '': # done with this group.
			count += count_answsers_1(declaration_map)
			# print(declaration_map)
			# print("next group")
			declaration_map = [0] * 26 # reset
			continue
		for i in range(0, len(line)):
			# print(line[i])
			index = ord(line[i]) - 97
			declaration_map[index] += 1
	# print(declaration_map)
	count += count_answsers_1(declaration_map)
	return count


result = find_1(lines)
print(result)

filename = "resources/input_6"
lines = get_lines(filename)

result = find_1(lines)
print("\nresult:", result)


print("\nPart 2:\n")

def count_answsers_2(declaration_map, group_size):
	count = 0
	for i in range(0, len(declaration_map)):
		if declaration_map[i] == group_size:
			count += 1
	return count

def find_2(lines):
	count = 0
	declaration_map = [0] * 26 # a to z
	group_size = 0
	for line in lines:
		if line == '': # done with this group.
			count += count_answsers_2(declaration_map, group_size)
			# print(declaration_map)
			# print(group_size)
			# print("next group")
			declaration_map = [0] * 26 # reset
			group_size = 0
			continue
		for i in range(0, len(line)):
			# print(line[i])
			index = ord(line[i]) - 97
			declaration_map[index] += 1
		group_size += 1
	# print(declaration_map)
	# print(group_size)
	count += count_answsers_2(declaration_map, group_size)
	return count

result = find_2(lines)
print("result:", result)
