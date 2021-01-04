# import itertools
import functools
import math

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_20"
filename = "resources/input_20"

############################################################
# Fetching data:

lines = get_lines(filename)

def get_tiles(lines):
	tiles, id_mode, tile_id, img = [], True, 0, []
	for line in lines:
		if line == '':
			tiles.append((tile_id, img))
			img = []
			id_mode = True
			continue
		elif id_mode == True:
			tile_id = int(line[line.find(" ") + 1 : -1])
			id_mode = False
		else:
			img.append(line)
	tiles.append((tile_id, img))
	return tiles

tiles = get_tiles(lines)
for tile in tiles:
	print(tile)

img_size = int(math.sqrt(len(tiles)))
print("\nimg_size:", img_size, "\n")

def print_tile(tile):
	print("\nTile id:", tile[0])
	for row in tile[1]:
		print(row)
	print()

############################################################
# Canonical representation:

# Careful, leading 0s will be removed!
def edge_to_int(edge):
	edge = edge.replace(".", "0")
	edge = edge.replace("#", "1")
	edge = int(edge)
	return edge

def get_edge_key(rot, edge):
	key, key_mirror = edge_to_int(edge), edge_to_int(edge[:: -1])
	if key < key_mirror:
		return rot, 0, key
	else:
		return rot, 1, key_mirror

s1 = "###.##.#.."
s2 = "..##.#..#."
print(s1, "->", get_edge_key(0, s1))
print(s2, "->", get_edge_key(0, s2))

concatenation = lambda strings : functools.reduce(lambda str1, str2 : str1 + str2, strings)

# Note: first value is the number of clockwise quarter turn
# needed to see the given edge top. Edges orientation must be
# invariant by rotation!
def get_tile_keys(tile_img):
	up = 0, tile_img[0]
	left = 1, concatenation([ row[0] for row in tile_img[:: -1] ])
	# left = 1, concatenation([ row[0] for row in tile_img ])
	down = 2, tile_img[-1][:: -1]
	right = 3, concatenation([ row[-1] for row in tile_img ])
	# print(up, left, down, right)
	return list(map(lambda c : get_edge_key(c[0], c[1]), [up, left, down, right]))

tile_expl = tiles[0]
# print_tile(tile_expl)
# keys_expl = get_tile_keys(tile_expl[1])
# print("its keys:", keys_expl, "\n")

tile_edges_map = list(map(lambda tile : (tile[0], get_tile_keys(tile[1])), tiles))

print("\ntile_edges_map:")
for keys in tile_edges_map:
	print(keys)

############################################################
# Matches search:

def search_matches(tile_edges_map, index):
	matches = []
	for i in range(len(tile_edges_map)):
		if i == index:
			continue
		for a in range(4):
			for b in range(4):
				key_index = tile_edges_map[index][1][a][2]
				key_i = tile_edges_map[i][1][b][2]
				if key_index == key_i:
					matches.append( ((index, a), (i, b), key_index) ) # N.B: a, b are rot values
	return matches

def build_match_list(tile_edges_map):
	match_list = []
	for index in range(len(tile_edges_map)):
		matches = search_matches(tile_edges_map, index)
		match_list.append(matches)
	return match_list

def build_sorted_match_list(tile_edges_map):
	return sorted(build_match_list(tile_edges_map), key=lambda c : len(c[1]))

match_list = build_match_list(tile_edges_map)
# sorted_match_list = build_sorted_match_list(tile_edges_map)

print("\nmatch_list:")
for match in match_list:
	print(match)

# print("\nsorted_match_list:")
# for match in sorted_match_list:
# 	print(match)

def build_match_matrix(tile_edges_map):
	n = len(tile_edges_map)
	matrix = [0] * n
	for index in range(n):
		matrix[index] = ["    "] * n # string for better printing. May be changed!
		matches = search_matches(tile_edges_map, index)
		for match in matches:
			a, b, key = match
			matrix[index][b[0]] = (a[1], b[1])
	return matrix

match_matrix = build_match_matrix(tile_edges_map) # twice too much work!

# print("\nmatch_matrix:")
# for row in match_matrix:
# 	print(row)

def get_id_from_index(index):
	return tile_edges_map[index][0]

is_corner = lambda index : len(match_list[index]) == 2

corners = []
mult = 1
for i in range(len(tile_edges_map)):
	matches = search_matches(tile_edges_map, i)
	if len(matches) == 2:
		tile_id = get_id_from_index(i)
		corners.append((i, tile_id))
		# print(tile_id)
		mult *= tile_id
print("\nresult:", mult, "\n")

############################################################
# Building the skeleton:

print("\nPart 2:\n")

def build_skeleton():
	skeleton, found_indexes = [0] * img_size, []
	# First row:
	skeleton[0] = [-1] * img_size
	skeleton[0][0] = corners[0][0] # first corner index
	found_indexes.append(skeleton[0][0])
	for col in range(1, img_size):
		prev_prev_index = skeleton[0][max(0, col-2)]
		prev_index = skeleton[0][col-1]
		# Find any j, index of a tile linked with previous_index, with j != previous_index and tile j not inside:
		diff_not_inside = lambda triple : triple[1][0] != prev_prev_index and len(match_list[triple[1][0]]) != 4
		not_inside = list(filter(diff_not_inside, match_list[prev_index]))
		skeleton[0][col] = not_inside[0][1][0]
		found_indexes.append(skeleton[0][col])
	# Last rows:
	for row in range(1, img_size):
		skeleton[row] = [-1] * img_size
		for col in range(0, img_size):
			up_index = skeleton[row-1][col]
			not_found = list(filter(lambda triple : not triple[1][0] in found_indexes, match_list[up_index]))
			skeleton[row][col] = not_found[0][1][0]
			found_indexes.append(skeleton[row][col])
	return skeleton

skeleton = build_skeleton()

for row in skeleton:
	print(row)
print()

for row in skeleton:
	print(list(map(lambda col : get_id_from_index(col), row)))
print()

############################################################
# Building the graphical representation:

def list_find(some_list, some_func):
	try:
		return list(filter(some_func, some_list))[0]
	except:
		print("Element not found.")
		return None

# print(list_find([1, 2, 3, 4], lambda x : x * x == 9))

def find_triple(current_index, prev_index):
	return list_find(match_list[current_index], lambda triple : triple[1][0] == prev_index)

def get_rot_sym_status(transf_matrix, prev_coord, curr_coord):
	prev_index = skeleton[prev_coord[0]][prev_coord[1]]
	current_index = skeleton[curr_coord[0]][curr_coord[1]]
	triple_prev = find_triple(current_index, prev_index)
	prev_edge_sym = tile_edges_map[prev_index][1][triple_prev[1][1]][1]
	current_edge_sym = tile_edges_map[current_index][1][triple_prev[0][1]][1]
	torque = prev_edge_sym == current_edge_sym
	prev_sym_status = bool(transf_matrix[prev_coord[0]][prev_coord[1]][1])
	rot_status = triple_prev[0][1]
	sym_status = int(prev_sym_status != torque)
	return rot_status, sym_status

def build_transformation_matrix():
	transf_matrix = [0] * img_size
	for i in range(img_size):
		transf_matrix[i] = [0] * img_size

	# Top left corner:
	index_corner = skeleton[0][0]
	index_corner_right = skeleton[0][1]
	index_corner_down = skeleton[1][0]
	triple_right = find_triple(index_corner, index_corner_right)
	triple_down = find_triple(index_corner, index_corner_down)
	transf_matrix[0][0] = ((triple_right[0][1] + 1) % 4, 1 - triple_down[0][1] // 2) # rot, sym

	# End of first row:
	for col in range(1, img_size):
		rot_status, sym_status = get_rot_sym_status(transf_matrix, (0, col-1), (0, col))
		transf_matrix[0][col] = ((rot_status - 1) % 4, sym_status)

	# Last rows:
	for row in range(1, img_size):
		for col in range(0, img_size):
			rot_status, sym_status = get_rot_sym_status(transf_matrix, (row-1, col), (row, col))
			transf_matrix[row][col] = ((rot_status + 2 * sym_status) % 4, sym_status)
			# +2 to convert vertical to horizontal symmetries, when needed.
	return transf_matrix

transf_matrix = build_transformation_matrix()

print("\ntransf_matrix:")
for row in transf_matrix:
	print(row)

############################################################
# Matrix transformations:

# Returns a new matrix. quarter_turn: clockwise
# Works on rectangular images.
def rotation(tile_img, quarter_turn):
	q = quarter_turn % 4
	if q % 2 == 0:
		n = len(tile_img)
	else:
		n = len(tile_img[0])
	copy = [0] * n
	if q == 1:
		for row in range(n):
			copy[row] = concatenation([ r[row] for r in tile_img[:: -1] ])
	elif q == 2:
		for row in range(n):
			copy[row] = concatenation(tile_img[-row-1][:: -1])
	elif q == 3:
		for row in range(n):
			copy[row] = concatenation([ r[-row-1] for r in tile_img ])
	else:
		for row in range(n):
			copy[row] = tile_img[row]
	return copy

# Returns a new matrix. quarter_turn: clockwise
# Works on rectangular images.
def symmetry(tile_img, symmetry_status, horizontal_status):
	n = len(tile_img)
	copy = [0] * n
	if symmetry_status == 1 and horizontal_status == 1:
		for row in range(n):
			copy[row] = tile_img[-row-1]
	elif symmetry_status == 1 and not horizontal_status == 1:
		for row in range(n):
			copy[row] = tile_img[row][:: -1]
	else:
		for row in range(n):
			copy[row] = tile_img[row]
	return copy

# print()
# for row in tile_expl[1]:
# 	print(row)
# print()
# for row in rotation(tile_expl[1], 1): # OK
# 	print(row)
# print()
# for row in rotation(tile_expl[1], 2): # OK
# 	print(row)
# print()
# for row in rotation(tile_expl[1], 3): # OK
# 	print(row)
# print()
# for row in symmetry(tile_expl[1], 0, 0): # OK
# 	print(row)
# print()
# for row in symmetry(tile_expl[1], 0, 1): # OK, shouldn't happen
# 	print(row)
# print()
# for row in symmetry(tile_expl[1], 1, 0): # OK
# 	print(row)
# print()
# for row in symmetry(tile_expl[1], 1, 1): # OK
# 	print(row)
# print()

############################################################
# Image construction:

def get_transf_tiles():
	transf_map = [0] * len(tiles)
	for i in range(img_size):
		for j in range(img_size):
			transf_map[skeleton[i][j]] = transf_matrix[i][j]
	# print("\ntransf_map:", transf_map, "\n")
	transf_tiles = [0] * len(tiles)
	for i in range(len(tiles)):
		r, s = transf_map[i]
		rotated = rotation(tiles[i][1], r)
		transf_tiles[i] = symmetry(rotated, s, 1) # only horizontal symmetries here.
		# transf_tiles[i] = rotated
	return transf_tiles

print()
transf_tiles = get_transf_tiles()

def build_pre_image():
	tile_size = len(tiles[0][1])
	image = [""] * img_size * (tile_size + 1)
	for i in range(img_size):
		for j in range(img_size):
			for k in range(tile_size):
				# image[i * (tile_size + 1) + k] += "  " + tiles[skeleton[i][j]][1][k] # before rot & sym.
				image[i * (tile_size + 1) + k] += "  " + transf_tiles[skeleton[i][j]][k]
	return image

pre_image = build_pre_image()

print()
for row in pre_image:
	print(row)
print()

def build_image():
	tile_size = len(tiles[0][1])
	image = [""] * img_size * tile_size
	offset = 0
	for i in range(img_size * (tile_size + 1)):
		if pre_image[i] == "":
			offset += 1
		elif (i - offset) % tile_size in [0, tile_size -1]:
			pass
		else:
			row = pre_image[i].split("  ")
			row = map(lambda chunk : chunk[1 : -1], row)
			image[i - offset] = concatenation(row)
	image = list(filter(lambda row : row != "", image))
	return image

image = build_image()

print("image:\n")
for row in image:
	print(row)
print()

############################################################
# Monster fishing:

monster_scan = ["                  # ",
				"#    ##    ##    ###",
				" #  #  #  #  #  #   "]

def monster_fits(kernel, curr_row, curr_col):
	kernel_height, kernel_width = len(kernel), len(kernel[0])
	for row in range(kernel_height):
		for col in range(kernel_width):
			if kernel[row][col] == '#' and image[curr_row + row][curr_col + col] != '#':
				return False
	return True

def search_kernel(kernel):
	height, width = len(image), len(image[0])
	kernel_height, kernel_width = len(kernel), len(kernel[0])
	count = 0
	for row in range(height - kernel_height + 1):
		for col in range(width - kernel_width + 1):
			if monster_fits(kernel, row, col):
				count += 1
	return count

def search_monster():
	for r in range(4):
		for s in range(2):
			kernel = symmetry(rotation(monster_scan, r), s, 1)
			count = search_kernel(kernel)
			if count > 0:
				print("\nr:", r, "s:", s)
				print("\nFound", count, "monsters!")
	return count

monsters = search_monster()

def roughness(image):
	return len(list(filter(lambda c : c == '#', concatenation(image))))

result = roughness(image) - monsters * roughness(monster_scan)
print("result:", result)
