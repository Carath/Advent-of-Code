# import time

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_7"
filename = "resources/input_7"

lines = get_lines(filename)


def parse_line(line):
	# print(line)
	words = line.split(" ")
	container = words[0], words[1]
	bags = []
	for i in range(4, len(words), 4):
		try:
			bag = int(words[i]), words[i+1], words[i+2]
			bags.append(bag)
		except Exception: # no other bags
			break
	return container, bags

# print(parse_line(lines[0]))

def list_adjective(lines):
	adjectives = []
	for line in lines:
		# print(line)
		container, bags = parse_line(line)
		if not container[0] in adjectives:
			adjectives.append(container[0])
		for bag in bags:
			if not bag[1] in adjectives:
				adjectives.append(bag[1])
	return adjectives

def list_colors(lines):
	colors = []
	for line in lines:
		# print(line)
		container, bags = parse_line(line)
		if not container[1] in colors:
			colors.append(container[1])
		for bag in bags:
			if not bag[2] in colors:
				colors.append(bag[2])
	return colors


# Those will be used to create the matrix map!
adjectives = list_adjective(lines)
colors = list_colors(lines)
print("adjectives: (len =", len(adjectives), "):\n\n", adjectives)
print("\ncolors: (len =", len(colors), "):\n\n", colors)


def get_map_index(adjective, color):
	return adjectives.index(adjective) * len(colors) + colors.index(color)

def get_adj_color(index):
	return adjectives[index // len(colors)], colors[index % len(colors)]

def create_matrix_map(adjectives, colors):
	n = len(adjectives) * len(colors)
	matrix_map = [[0] * n for i in range(n)]
	for line in lines:
		container, bags = parse_line(line)
		row = get_map_index(container[0], container[1])
		for bag in bags:
			col = get_map_index(bag[1], bag[2])
			matrix_map[row][col] = bag[0]
	return matrix_map

def print_matrix(matrix):
	for row in matrix:
		print(row)

matrix = create_matrix_map(adjectives, colors)


def find_containing(adjective, color):
	col = get_map_index(adjective, color)
	row_list = []
	next_index = 0
	while True:
		for row in range(0, len(matrix)):
			if matrix[row][col] > 0 and not row in row_list:
				row_list.append(row)
		if (next_index >= len(row_list)):
			break
		col = row_list[next_index]
		next_index += 1
	row_list = list(map(get_adj_color, row_list))
	return row_list

row_list = find_containing("shiny", "gold")
print("\ncontainging shiny gold:\n\n", row_list)
print("\nresult:", len(row_list))


print("\nPart 2:\n")

def compute_content(matrix):
	# start = time.time_ns()
	weights = [1] * len(matrix)
	index_range = range(0, len(matrix))
	get_rows_weights_used = lambda row : list(filter(lambda i : matrix[row][i] > 0, index_range))
	list_rows_weights_used = list(map(get_rows_weights_used, index_range))
	rows_known_weights = []
	while len(rows_known_weights) < len(matrix):
		for row in index_range:
			if (not row in rows_known_weights) and set(list_rows_weights_used[row]) <= set(rows_known_weights):
				for row_weight in list_rows_weights_used[row]:
					weights[row] += matrix[row][row_weight] * weights[row_weight]
				rows_known_weights.append(row)
	weights = list(map(lambda x : x-1, weights))
	# elapsed = (time.time_ns() - start) / 1e9
	# print("Time: " + str(elapsed) + " s")
	return weights

# Variant:
def compute_content_2(matrix):
	start = time.time_ns()
	weights = [1] * len(matrix)
	index_range = list(range(0, len(matrix)))
	get_rows_weights_used = lambda row : list(filter(lambda i : matrix[row][i] > 0, index_range))
	list_rows_weights_used = list(map(get_rows_weights_used, index_range))
	rows_unknown_weights = index_range
	while rows_unknown_weights != []:
		for row in rows_unknown_weights:
			if set(list_rows_weights_used[row]).isdisjoint(set(rows_unknown_weights)):
				for row_weight in list_rows_weights_used[row]:
					weights[row] += matrix[row][row_weight] * weights[row_weight]
				rows_unknown_weights.remove(row)
	weights = list(map(lambda x : x-1, weights))
	elapsed = (time.time_ns() - start) / 1e9
	print("Time: " + str(elapsed) + " s")
	return weights


weights = compute_content(matrix)
# weights = compute_content_2(matrix)
# print("weights: " + str(weights))

result = weights[get_map_index("shiny", "gold")]
print("result:", result)
