print("\nPart 2:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_17"
filename = "resources/input_17"

lines = get_lines(filename)
init_size = len(lines[0])
# print(lines)


# Parameter:
epoch_number = 6

def get_size(dim_init_size):
	return dim_init_size + 2 * (epoch_number + 1) # do not modify!

size_x = get_size(init_size)
size_y = get_size(init_size)
size_z = get_size(1)
size_w = get_size(1)

def coord(i):
	return i + epoch_number + 1

def projection(x, y):
	return (coord(0), coord(0), coord(y), coord(x))

# Warning (w, z, y, x) coordinates used!
def fill_matrix(lines):
	# Allocating:
	matrix = [0] * size_w
	for i in range(size_w):
		matrix[i] = [0] * size_z
		for j in range(size_z):
			matrix[i][j] = [0] * size_y
			for k in range(size_y):
				matrix[i][j][k] = ['.'] * size_x
	# Filling:
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			matrix[coord(0)][coord(0)][coord(i)][coord(j)] = lines[i][j]
	return matrix

def print_matrix(matrix, layer):
	z = coord(layer)
	for row in matrix[z]:
		print(row)
	print()

def deep_copy_matrix(matrix):
	return [ [ [ c[:] for c in col ] for col in row ] for row in matrix]

matrix = fill_matrix(lines)
# print_matrix(matrix, 0)


# Note: every function below assume enough headroom at the matrix edges.

def count_all_active(matrix):
	count = 0
	for i in range(size_w):
		for j in range(size_z):
			for k in range(size_y):
				for l in range(size_x):
					if matrix[i][j][k][l] == '#':
						count += 1
	return count

# Careful, point must not be on the map bounds!
def count_active_neighbours(matrix, point):
	w, z, y, x = point
	count = 0
	for i in range(w-1, w+2):
		for j in range(z-1, z+2):
			for k in range(y-1, y+2):
				for l in range(x-1, x+2):
					if matrix[i][j][k][l] == '#':
						count += 1
	if matrix[w][z][y][x] == '#':
		count -= 1
	return count

# count = count_active_neighbours(matrix, projection(1, 1))
# print("count:", count)

def forward(matrix, pass_number):
	for p in range(pass_number):
		copy = deep_copy_matrix(matrix)
		for i in range(1, size_w - 1):
			for j in range(1, size_z - 1):
				for k in range(1, size_y - 1):
					for l in range(1, size_x - 1):
						count = count_active_neighbours(copy, (i, j, k, l))
						if copy[i][j][k][l] == '#' and not count in range(2, 4):
							matrix[i][j][k][l] = '.'
						elif copy[i][j][k][l] == '.' and count == 3:
							matrix[i][j][k][l] = '#'

forward(matrix, 6)
# print_matrix(matrix, 0)
result = count_all_active(matrix)
print("result:", result)
