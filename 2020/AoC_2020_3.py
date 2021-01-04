print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

def count_trees_slope(lines, x, y):
	rows, cols = len(lines), len(lines[0])
	count, row, col = 0, 0, 0
	while row < rows:
		if lines[row][col] == "#":
			# print(row, col)
			count += 1
		row += y
		col = (col + x) % cols
	return count

lines = get_lines("resources/example_3")

result = count_trees_slope(lines, 3, 1)
print("result", result)

lines = get_lines("resources/input_3")

result = count_trees_slope(lines, 3, 1)
print("\nresult", result)


print("\nPart 2:\n")

result *= count_trees_slope(lines, 1, 1)
result *= count_trees_slope(lines, 5, 1)
result *= count_trees_slope(lines, 7, 1)
result *= count_trees_slope(lines, 1, 2)

print("result", result)
