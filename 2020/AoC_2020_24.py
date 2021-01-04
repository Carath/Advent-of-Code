import functools

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_24"
filename = "resources/input_24"

lines = get_lines(filename)

############################################################
# Getting instructions:

direction_list = ["nw", "ne", "w", "e", "sw", "se"] # hex grid

def get_coord_next(key):
	switcher = {
		"nw": (-1, 0),
		"ne": (-1, 1),
		"w" : (0, -1),
		"e" : (0, 1),
		"sw": (1, -1),
		"se": (1, 0),
	}
	return switcher.get(key, "Invalid key")

def get_directions(string):
	directions, i, j = [], 0, 0
	while i < len(string):
		while j < len(string) and not string[i : j] in direction_list:
			j += 1
		directions.append(string[i : j])
		i = j
	return directions

instructions = list(map(get_directions, lines))

print("Instructions number:", len(instructions))
# for row in instructions:
# 	print(row)
# print()

############################################################
# Parameter to be set beforehand:

max_epoch_number = 100

############################################################
# Counting the active tiles, computing the optimal sizes,
# and creating the grid:

def get_init_active_tiles():
	init_active_tiles = []
	for instr in instructions:
		dest = (0, 0)
		for direc in instr:
			coord_next = get_coord_next(direc)
			dest = (dest[0] + coord_next[0], dest[1] + coord_next[1])
		if dest in init_active_tiles:
			init_active_tiles.remove(dest)
		else:
			init_active_tiles.append(dest)
	return init_active_tiles

init_active_tiles = get_init_active_tiles()
print("Initial active tiles number:", len(init_active_tiles))


# Get the optimal size and shift for a grid, in function
# of the init shape and the maximum number of epochs:
def get_dimensions():
	unziped = list(zip(*init_active_tiles))
	row_min, row_max = min(unziped[0]), max(unziped[0])
	col_min, col_max = min(unziped[1]), max(unziped[1])
	# print(row_min, col_min, row_max, col_max)
	margin = max_epoch_number + 1
	size_row = row_max - row_min + 2 * margin
	size_col = col_max - col_min + 2 * margin
	shift_row = margin - row_min
	shift_col = margin - col_min
	return size_row, size_col, shift_row, shift_col

size_row, size_col, shift_row, shift_col = get_dimensions()
print("Grid size:", size_row, "x", size_col)

idx_from_raw_coord = lambda row, col : (row + shift_row) * size_col + col + shift_col

def create_grid():
	grid = [0] * size_row * size_col
	for coord in init_active_tiles:
		grid[idx_from_raw_coord(*coord)] = 1
	return grid

grid = create_grid()

is_active = lambda idx : grid[idx] == 1
concatenation = lambda strings : functools.reduce(lambda str1, str2 : str1 + str2, strings)
status_tochar = lambda status : '#' if (status == 1) else '.'

def print_grid(grid_used):
	print("\ngrid:\n")
	for row in range(size_col):
		grid_row = grid_used[row * size_col : (row + 1) * size_col]
		string = concatenation(map(status_tochar, grid_row))
		print(string)
	print()

# print_grid(grid)

############################################################
# Iterating:

print("\nPart 2:\n")

def get_neighbours(idx):
	return [idx - size_col, idx - size_col + 1, idx - 1, idx + 1, idx + size_col - 1, idx + size_col]

# This should only be run once:
def run(epoch_number):
	if epoch_number > max_epoch_number:
		print("Too much epochs to do (" + str(epoch_number) + "): increase 'max_epoch_number'.")
		return
	# Setup:
	candidates = set()
	for coord in init_active_tiles:
		index = idx_from_raw_coord(*coord)
		neighbours = get_neighbours(index)
		candidates.update([index], neighbours)
	# Runtime:
	for epoch in range(epoch_number):
		# Copying to avoid side effects:
		grid_copy = grid[:]
		copy_candidates = candidates.copy()
		was_active = lambda idx : grid_copy[idx] == 1
		for index in copy_candidates:
			status = was_active(index)
			neighbours = get_neighbours(index)
			count = len(list(filter(was_active, neighbours)))
			if status and (count == 0 or count > 2): # tile goes inactive.
				grid[index] = 0
				# Do not remove 'index' from candidates!
			elif not status and count == 2: # tile goes active.
				grid[index] = 1
				candidates.update(neighbours) # 'index' already in candidates!
	return list(filter(is_active, list(candidates)))

active_tiles = run(max_epoch_number)
# print_grid(grid)
print("Active tiles number:", len(active_tiles))
