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
max_epoch_number = 6

def get_size(dim_init_size):
	return dim_init_size + 2 * (max_epoch_number + 1) # do not modify!

size_x = get_size(init_size)
size_y = get_size(init_size)
size_z = get_size(1)
size_w = get_size(1)

def coord(i):
	return i + max_epoch_number + 1

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
	init_active_tiles = []
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			w, z, y, x = coord(0), coord(0), coord(i), coord(j)
			matrix[w][z][y][x] = lines[i][j]
			if lines[i][j] == '#':
				init_active_tiles.append((w, z, y, x))
	return matrix, init_active_tiles

def print_matrix(matrix, layer):
	z = coord(layer)
	for row in matrix[z]:
		print(row)
	print()

def deep_copy_matrix(matrix):
	return [ [ [ c[:] for c in col ] for col in row ] for row in matrix]

matrix, init_active_tiles = fill_matrix(lines)
# print_matrix(matrix, 0)


# Note: every function below assume enough headroom at the matrix edges.

# Careful, point must not be on the map bounds!
def get_neighbours(coord):
	w, z, y, x = coord
	neighbours = []
	for i in range(w-1, w+2):
		for j in range(z-1, z+2):
			for k in range(y-1, y+2):
				for l in range(x-1, x+2):
						neighbours.append((i, j, k, l))
	neighbours.remove(coord)
	return neighbours

is_active = lambda c : matrix[c[0]][c[1]][c[2]][c[3]] == '#'

# This should only be run once:
def run(epoch_number):
	if epoch_number > max_epoch_number:
		print("Too much epochs to do (" + str(epoch_number) + "): increase 'max_epoch_number'.")
		return
	# Setup:
	candidates = set()
	for coord in init_active_tiles:
		neighbours = get_neighbours(coord)
		candidates.update([coord], neighbours)
	# Runtime:
	for epoch in range(epoch_number):
		# Copying to avoid side effects:
		matrix_copy = deep_copy_matrix(matrix)
		copy_candidates = candidates.copy()
		was_active = lambda c : matrix_copy[c[0]][c[1]][c[2]][c[3]] == '#'
		for coord in copy_candidates:
			i, j, k, l = coord
			status = was_active(coord)
			neighbours = get_neighbours(coord)
			count = len(list(filter(was_active, neighbours)))
			if status and not count in range(2, 4): # tile goes inactive.
				matrix[i][j][k][l] = '.'
				# Do not remove 'coord' from candidates!
			elif not status and count == 3: # tile goes active.
				matrix[i][j][k][l] = '#'
				candidates.update(neighbours) # 'coord' already in candidates!
	return list(filter(is_active, list(candidates)))

active_tiles = run(max_epoch_number)
print("Active tiles number:", len(active_tiles))
