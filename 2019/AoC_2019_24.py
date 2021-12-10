import sys
sys.path.insert(0, '../2020/')
from AoC_2020_24_dict import GameOfLife

def stringToCellsList(string):
	rows = list(filter(lambda s : s != '', string.split('\n')))
	cellsList = []
	for row in range(len(rows)):
		cellsRow = list(filter(lambda c : c[1] == '#', enumerate(rows[row])))
		cellsRow = [ (c[0], row, 0) for c in cellsRow ]
		cellsList.extend(cellsRow)
	return cellsList

def getCells(game, string):
	cellsList = stringToCellsList(string)
	cells = {}
	for c in cellsList:
		game.addCell(cells, c)
	return cells

# Only keeping alive cells, and sorted to have a unique representation:
def cellsToCellsList(cells):
	aliveCells = filter(lambda cell : cell[1], cells.items())
	return sorted([ cell[0] for cell in aliveCells ])

def cellsToString(cells):
	cellsList = cellsToCellsList(cells)
	return ','.join([ str(cell) for cell in cellsList ])

def getCellsGrid(cells, zLevel):
	grid = [ ['.'] * 5 for row in range(5)]
	for c in cells:
		x, y, z = c
		if z == zLevel and cells[c]:
			grid[y][x] = '#'
	return grid

def printCells(cells, zLevel):
	grid = getCellsGrid(cells, zLevel)
	print('\n' + '\n'.join([ ''.join(row) for row in grid ]) + '\n')

# Rule governing the life and death of a cell, knowing its status
# and the number of alive neighbour cells.
def rules(status, count):
	if status and count != 1: # cell dies.
		return -1
	elif not status and (count == 1 or count == 2): # cell lives!
		return 1
	return 0 # cell doesn't change.

# Peculiar neighbourhood on a 5x5 grid:
def neighbourhood(x, y, z):
	neighbours = [(x-1, y, z), (x, y-1, z), (x, y+1, z), (x+1, y, z)]
	return list(filter(lambda c : 0 <= c[0] and c[0] < 5 and 0 <= c[1] and c[1] < 5, neighbours))

def detectRedundancy(game, cells):
	history, epoch = {}, 0
	while True:
		# The following string uniquely define the current state, since cellsToCellsList()
		# keeps only alive cells, sorted by lexicographic order on x, y, z.
		string = cellsToString(cells)
		if string in history:
			print('\nRedundancy found at epoch %d:\n' % epoch, string)
			return history[string]
		history[string] = cells.copy()
		game.run(cells, 1, enableCleanup=False)
		epoch += 1

def computeRating(cells):
	rating = 0
	for c in cells:
		if cells[c]:
			rating += 1 << (c[1] * 5 + c[0])
	return rating

# inputData = '''
# ....#
# #..#.
# #..##
# ..#..
# #....
# '''

inputData = '''
#.#.#
..#..
.#.##
.####
###..
'''

game = GameOfLife(rules, neighbourhood)

cells = getCells(game, inputData)
print('\ncells:', cells)

printCells(cells, 0)
print('String identifier:', cellsToString(cells))

redundancy = detectRedundancy(game, cells)
print(redundancy)

print('\nBiodiversity rating:', computeRating(redundancy), '\n') # 14539258

# ------------------------------------------
# Part 2:

def leftNeighbors(x, y, z):
	if x == 0:
		return [(1, 2, z-1)]
	if x == 3 and y == 2:
		return [(4, i, z+1) for i in range(5)]
	return [(x-1, y, z)]

def rightNeighbors(x, y, z):
	if x == 4:
		return [(3, 2, z-1)]
	if x == 1 and y == 2:
		return [(0, i, z+1) for i in range(5)]
	return [(x+1, y, z)]

def upNeighbors(x, y, z):
	if y == 0:
		return [(2, 1, z-1)]
	if x == 2 and y == 3:
		return [(i, 4, z+1) for i in range(5)]
	return [(x, y-1, z)]

def downNeighbors(x, y, z):
	if y == 4:
		return [(2, 3, z-1)]
	if x == 2 and y == 1:
		return [(i, 0, z+1) for i in range(5)]
	return [(x, y+1, z)]

# Infinite recursive grid!
def neighbourhoodRecursive(x, y, z):
	l = []
	l.extend(leftNeighbors(x, y, z))
	l.extend(rightNeighbors(x, y, z))
	l.extend(upNeighbors(x, y, z))
	l.extend(downNeighbors(x, y, z))
	return l

gameRecursive = GameOfLife(rules, neighbourhoodRecursive)

cells = getCells(gameRecursive, inputData)
gameRecursive.run(cells, 200)

aliveCellsNumber = gameRecursive.countAliveCells(cells)
print('\nResult:', aliveCellsNumber) # 1977
