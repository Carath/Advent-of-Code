# import time

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_11"
# filename = "resources/example_11_2"
filename = "resources/input_11"

lines = get_lines(filename)
# print(lines)

def fill_matrix(lines):
	matrix = [0] * len(lines)
	for i in range(len(lines)):
		matrix[i] = [0] * len(lines[i])
		for j in range(len(lines[i])):
			matrix[i][j] = lines[i][j]
	return matrix

def get_copy_matrix(matrix):
	return [row[:] for row in matrix]

def print_matrix(matrix):
	for row in matrix:
		print(row)
	print()

matrix = fill_matrix(lines)
# print_matrix(matrix)

def count_adj_occupied(matrix, row, col):
	height, width = len(matrix), len(matrix[0])
	row_start, row_end = max(0, row-1), min(height-1, row+1)
	col_start, col_end = max(0, col-1), min(width-1, col+1)
	count = 0
	for curr_row in range(row_start, row_end + 1):
		for curr_col in range(col_start, col_end + 1):
			if (curr_row != row or curr_col != col) and matrix[curr_row][curr_col] == '#':
				count += 1
	return count

def one_pass(neighbouring_fun, threshold):
	copy_matrix = get_copy_matrix(matrix)
	height, width = len(matrix), len(matrix[0])
	change_number = 0
	for row in range(height):
		for col in range(width):
			if copy_matrix[row][col] == '.':
				continue # small optimization: not computing the neighbours here.
			number_adj_occupied = neighbouring_fun(copy_matrix, row, col)
			# print(number_adj_occupied)
			if copy_matrix[row][col] == 'L' and number_adj_occupied == 0:
				matrix[row][col] = '#'
				change_number += 1
			elif copy_matrix[row][col] == '#' and number_adj_occupied >= threshold:
				matrix[row][col] = 'L'
				change_number += 1
	# print_matrix(matrix)
	return change_number

# one_pass(count_adj_occupied, 4)
# one_pass(count_adj_occupied, 4)

def run(neighbouring_fun, threshold):
	# start = time.time_ns()
	epoch_number = 0
	while one_pass(neighbouring_fun, threshold) > 0:
		epoch_number += 1
	# print_matrix(matrix)
	# elapsed = (time.time_ns() - start) / 1e9
	# print("Time:", elapsed, "s")
	print("Epoch number:", epoch_number)

def count_occupied():
	count = 0
	for i in range(len(matrix)):
		count += len(list(filter(lambda c : c == '#', matrix[i])))
	return count

run(count_adj_occupied, 4)
result = count_occupied()
print("\nresult:", result)


print("\nPart 2:\n")

def has_occupied_dir(matrix, row, col, row_shift, col_shift):
	curr_row, curr_col = row, col
	while True:
		curr_row += row_shift
		curr_col += col_shift
		if not (0 <= curr_row and curr_row < len(matrix) and 0 <= curr_col and curr_col < len(matrix[0])):
			return 0
		elif matrix[curr_row][curr_col] == '.':
			continue
		elif matrix[curr_row][curr_col] == '#':
			return 1
		else: # 'L'
			return 0

def count_adj_occupied_2(matrix, row, col):
	count = 0
	count += has_occupied_dir(matrix, row, col, -1, 0)
	count += has_occupied_dir(matrix, row, col, 1, 0)
	count += has_occupied_dir(matrix, row, col, 0, -1)
	count += has_occupied_dir(matrix, row, col, 0, 1)
	count += has_occupied_dir(matrix, row, col, -1, -1)
	count += has_occupied_dir(matrix, row, col, -1, 1)
	count += has_occupied_dir(matrix, row, col, 1, -1)
	count += has_occupied_dir(matrix, row, col, 1, 1)
	return count

# print(count_adj_occupied_2(matrix, 4, 3)) # to test on example_11_2

matrix = fill_matrix(lines) # reset
run(count_adj_occupied_2, 5)
result = count_occupied()
print("\nresult:", result)
