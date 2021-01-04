from functools import reduce

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_10_1"
# filename = "resources/example_10_2"
filename = "resources/input_10"

lines = get_lines(filename)
lines = list(map(lambda s : int(s), lines))

sorted_list = lines
sorted_list.append(0)
sorted_list.append(max(lines) + 3)
sorted_list = sorted(lines)
print(sorted_list)


def count(sorted_list):
	counts = [0] * 3
	for i in range(1, len(sorted_list)):
		delta = sorted_list[i] - sorted_list[i - 1]
		# print(delta)
		counts[delta - 1] += 1
	return counts

counts = count(sorted_list)
result = counts[0] * counts[2]
print(counts)
print("\nresult:", result)


print("\nPart 2:\n")

# Method 1 - hardcoded
# Uses the fact that delta subsets are only composed of 1 and of size <= 3...

def get_deltas(sorted_list):
	deltas = [0] * (len(sorted_list) - 1)
	for i in range(0, len(sorted_list) - 1):
		deltas[i] = sorted_list[i + 1] - sorted_list[i]
	return deltas

deltas = get_deltas(sorted_list)
print(deltas)


def get_subsets_count(deltas):
	subsets_count = []
	count = 0
	for i in range(1, len(deltas)):
		if deltas[i] == 1 and deltas[i - 1] < 3 and deltas[i] < 3:
			count += 1
		elif count > 0:
			subsets_count.append(count)
			count = 0
	return subsets_count

subsets_count = get_subsets_count(deltas)
# print(subsets_count)


# Values found by hand:
def get_value_hardcoded(count):
	if count == 1:
		return 2
	elif count == 2:
		return 4
	elif count == 3:
		return 7
	elif count == 4:
		return 13
	else:
		print("Unsupported case!")
		exit(1)

def get_result_hardcoded(subsets_count):
	return reduce(lambda x, y : x * y, map(get_value_hardcoded, subsets_count))

result = get_result_hardcoded(subsets_count)
print("\nresult:", result)


# Method 2 - general method

def get_value(subset):
	# print(subset)
	count = 1
	sublists, sublists_next = [subset], []
	while sublists != []:
		for current_subset in sublists:
			for i in range(0, len(current_subset) - 1):
				new_value = current_subset[i] + current_subset[i + 1]
				if new_value <= 3: # value at index i can be removed
					subcurrent_subset = current_subset[0 : i] + [new_value] + current_subset[i+2 : ]
					# print(subcurrent_subset)
					if not subcurrent_subset in sublists_next:
						sublists_next.append(subcurrent_subset)
		sublists, sublists_next = sublists_next, []
		count += len(sublists)
		# print(sublists)
	# print(count)
	return count

# count = get_value([1, 1])
# count = get_value([1, 1, 1])
# count = get_value([1, 1, 1, 1])
# count = get_value([1, 1, 1, 1, 1])
# count = get_value([1, 2, 1, 1])
# count = get_value([1, 1, 1, 2])


def get_subsets(deltas):
	subsets = []
	i = 0
	while i < len(deltas):
		while i < len(deltas) and deltas[i] == 3:
			i += 1
		j = i
		while j < len(deltas) and deltas[j] != 3:
			j += 1
		# print(deltas[i : j])
		subsets.append(deltas[i : j])
		i = j + 1
	return subsets

def get_result_general(subsets):
	return reduce(lambda x, y : x * y, map(get_value, subsets))

subsets = get_subsets(deltas)
# print(subsets)
result = get_result_general(subsets)
print("\nresult:", result)
