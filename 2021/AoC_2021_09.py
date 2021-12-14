def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

inputData = getFileLines('resources/input_09.txt')
inputData = list(filter(lambda s : s != '', inputData))
# print('inputData:', inputData)

def neighbourhood(row, col, rows, cols):
	isInGrid = lambda coord : coord[0] in range(rows) and coord[1] in range(cols)
	neighbors = [(row-1, col), (row, col-1), (row, col+1), (row+1, col)]
	return list(filter(isInGrid, neighbors))

def findLowPoints(grid):
	lowPoints = []
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			neighbors = neighbourhood(row, col, len(grid), len(grid[0]))
			isLowPoint = True
			for neighbor in neighbors:
				if grid[row][col] >= grid[neighbor[0]][neighbor[1]]:
					isLowPoint = False
					break
			if isLowPoint:
				lowPoints.append((row, col))
	return lowPoints

lowPoints = findLowPoints(inputData)
print('\nLow points:', lowPoints)

def computeRiskLevel(grid, lowPoints):
	theSum = 0
	for coord in lowPoints:
		theSum += 1 + int(grid[coord[0]][coord[1]])
	return theSum

result = computeRiskLevel(inputData, lowPoints)
print('\nResult:', result, '\n') # 500

# ------------------------------------------
# Part 2:

def findBasin(grid, ref):
	currentHeight = grid[ref[0]][ref[1]]
	neighbors = neighbourhood(ref[0], ref[1], len(grid), len(grid[0]))
	isInSameBasin = lambda coord : grid[coord[0]][coord[1]] != '9' and grid[coord[0]][coord[1]] > currentHeight
	basin = set(filter(isInSameBasin, neighbors))
	for neighbor in basin.copy():
		basin.update(findBasin(grid, neighbor))
	basin.add(ref)
	return basin

def findBasins(grid, lowPoints):
	basins = []
	for coord in lowPoints:
		basins.append(findBasin(grid, coord))
	return basins

basins = findBasins(inputData, lowPoints)
# print('Basins:', *basins, sep='\n')

def computeResult(basins):
	basins = sorted(basins, key=len)
	m = 1
	for basin in basins[-3:]:
		m *= len(basin)
	return m

print('\nResult:', computeResult(basins)) # 970200
