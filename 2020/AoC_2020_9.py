print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

filename = "resources/example_9"
lines = get_lines(filename)
lines = list(map(lambda s : int(s), lines))

# N.B: Hash map impractical: too much memory used!
def find_intruder(lines, header_len):
	# Creating the list:
	number_list = []
	for i in range(0, header_len):
		for j in range(i+1, header_len):
			number_list.append(lines[i] + lines[j])
	# Searching for the intruder:
	rank = header_len
	while lines[rank] in number_list:
		# Adding and removing some sums:
		start = rank - header_len
		for j in range(start + 1, rank):
			number_list.remove(lines[j] + lines[start])
			number_list.append(lines[j] + lines[rank])
		rank += 1
	return lines[rank]


result = find_intruder(lines, 5)
print(result)

filename = "resources/input_9"
lines = get_lines(filename)
lines = list(map(lambda s : int(s), lines))

result = find_intruder(lines, 25)
print("\nresult:", result)


print("\nPart 2:\n")

# N.B: python seems to handle automatically integer sizes greater than 4 bytes...

def find_subset(lines, target_value):
	subset_size = 2
	while True:
		# First subset:
		subset_sum = 0
		for i in range(0, subset_size):
			subset_sum += lines[i]
		if subset_sum == target_value:
			return True, subset_size, rank
		# Other subsets, ranks reindexed from 0:
		for rank in range(0, len(lines) - subset_size):
			subset_sum -= lines[rank]
			subset_sum += lines[rank + subset_size]
			if subset_sum == target_value:
				return True, subset_size, rank + 1
		subset_size += 1
	return False, 0, 0


def find_sum(lines, answer):
	_, subset_size, rank = answer
	subset = lines[rank : rank + subset_size]
	print("subset size: " + str(subset_size))
	return min(subset) + max(subset)

result = find_sum(lines, find_subset(lines, result))
print("\nresult:", result)
