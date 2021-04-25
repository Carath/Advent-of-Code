############################################################
# Low memory footprint version!

# The Game of Life implemented here is generic, in that custom rules and neighbourhoods may be given.
# It only assumes two things:
# - A cell change of status only depends on (its status and) the number of its live neighbours;
# - Unless manually added, a cell cannot become alive without at least one of its neighbours being alive.

# The code here uses dictionaries, in order to access and add cells in amortized O(1), while using less memory
# than storing them in a simpler array/matrix, which would make RAM usage dependent on the distance between live
# cells. Concretely, used RAM should be roughly proportional to the number of live cells, and the extra memory used
# can be freed periodically.

# Remarks:
# - Cells change of status do not depend on the order in which they are parsed - they evolve simultaneously.
# - One cannot remove a dead cell from the dictionary in the midst of an epoch, even if none of its neighbours are
#   alive, for some of them may become alive later in the same epoch, thus potentially allowing the lone cell to live.
# - A cell is stored as a pair (key, value), where the key is the cell 2D coordinates, and the value is the cell status,
#   stored as a boolean.
# - Be careful to not manually set a cell to life by doing 'cells[coord] = True', as this will not consider the cell
#   neighbourhood! Use the 'addCell(cells, coord)' function instead.

############################################################

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
# print(*instructions, sep='\n')

def init(cells, instructions):
	for instr in instructions:
		dest = (0, 0)
		for direc in instr:
			coord_next = get_coord_next(direc)
			dest = (dest[0] + coord_next[0], dest[1] + coord_next[1])
		if isAlive(cells, dest):
			cells[dest] = False
		else:
			addCell(cells, dest)

############################################################
# Generic functions:

isAlive = lambda cells, coord : coord in cells and cells[coord]
countAliveCells = lambda cells : countAliveFromCoords(cells, cells.keys())

def countAliveFromCoords(cells, coordList):
	count = 0
	for coord in coordList:
		if isAlive(cells, coord):
			count += 1
	return count

def addCell(cells, coord):
	neighbours = neighbourhood(*coord)
	activate(cells, coord, neighbours)

def activate(cells, coord, neighbours):
	cells[coord] = True
	for c in neighbours:
		if not c in cells:
			cells[c] = False

def updateCell(cells, coord, status, count, neighbours):
	r = rules(status, count)
	if r == -1: # cell goes dead. Do not remove it!
		cells[coord] = False
	elif r == 1: # cell goes live.
		activate(cells, coord, neighbours)

def cleanupCell(cells, coord, status, count, neighbours):
	if not status and count == 0:
		del cells[coord]

# Removing totally dead cells. This _cannot_ be done while updating the cells
# without creating side effects. Also, note that this is somewhate expensive,
# better do it only once in a while to free memory:
def cleanup(cells):
	size = len(cells.keys())
	apply(cells, cleanupCell)
	print("Freed", size - len(cells.keys()), "cells.")

# Apply an action simultaneously on each cell, without side effects:
def apply(cells, action):
	cellsCopy = cells.copy()
	for coord in cellsCopy:
		neighbours = neighbourhood(*coord)
		status = isAlive(cellsCopy, coord)
		count = countAliveFromCoords(cellsCopy, neighbours)
		action(cells, coord, status, count, neighbours)

def run(cells, epochsNumber, cleanupCooldown):
	for epoch in range(epochsNumber):
		if epoch % cleanupCooldown == 0:
			cleanup(cells)
		apply(cells, updateCell)
	cleanup(cells)

############################################################
# Problem dependant:

# Rule governing the life and death of a cell, knowing its status
# and the number of alive neighbour cells.
def rules(status, count):
	if status and (count == 0 or count > 2): # cell dies.
		return -1
	elif not status and count == 2: # cell lives!
		return 1
	return 0 # cell doesn't change.

# Hexagonal neighbourhood, mapped to a regular grid:
def neighbourhood(x, y):
	return [(x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y)]

############################################################
# Printing:

concatenation = lambda strings : functools.reduce(lambda str1, str2 : str1 + str2, strings)

# Printing every live cells from a rectangle starting from the top left corner (x, y):
def printCurrentState(cells, x, y, width, height):
	# Initializing the grid:
	grid = ['.'] * height
	for i in range(height):
		grid[i] = ['.'] * width
	# Filling the grid with live cells:
	for coord in cells:
		if cells[coord]:
			col, row = coord[0] - x, coord[1] - y
			if 0 <= row and row < height and 0 <= col and col < width:
				grid[row][col] = '#'
	# Printing the result:
	print('', *map(concatenation, grid), '', sep='\n')

############################################################
# Testing:

cells = {}
init(cells, instructions)
printCurrentState(cells, -20, -20, 40, 40)
print("Alive cells number:", countAliveCells(cells))

print("\nPart 2:\n")

epochsNumber = 100 # output: 3711
# epochsNumber = 250 # output: 17038
cleanupCooldown = 50

run(cells, epochsNumber, cleanupCooldown)
print("Alive cells number:", countAliveCells(cells))
