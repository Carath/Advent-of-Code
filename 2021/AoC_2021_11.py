def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

def getGrid(string):
	grid = [ list(s) for s in string.split('\n') if s != '' ]
	grid = [ [ int(col) for col in row ] for row in grid ]
	return grid

isInGrid = lambda row, col : row in range(len(grid)) and col in range(len(grid[0]))

def neighbourhood(row, col):
	neighbors = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			if isInGrid(row+i, col+j):
				if i != 0 or j != 0:
					neighbors.append((row+i, col+j))
	return neighbors

def riseEnergyLevel(grid, hasExploded, coord):
	flashesNumber = 0
	grid[coord[0]][coord[1]] += 1
	if grid[coord[0]][coord[1]] > 9 and not coord in hasExploded:
		flashesNumber += 1
		hasExploded.add(coord)
		neighbors = neighbourhood(coord[0], coord[1])
		for neighbor in neighbors:
			flashesNumber += riseEnergyLevel(grid, hasExploded, neighbor)
	return flashesNumber

def run(grid, steps, stopAtSimultaneousFlashes=False):
	sumFlashesNumber, step = 0, 0
	tilesNumber = len(grid) * len(grid[0])
	while stopAtSimultaneousFlashes or step < steps:
		stepFlashesNumber, step = 0, step + 1
		hasExploded = set()
		for row in range(len(grid)):
			for col in range(len(grid[0])):
				stepFlashesNumber += riseEnergyLevel(grid, hasExploded, (row, col))
		sumFlashesNumber += stepFlashesNumber
		for coord in hasExploded:
			grid[coord[0]][coord[1]] = 0 # exploded ones cannot refill during this step!
		# print('Step: %d\n' % step, *grid, '', sep='\n')
		if stopAtSimultaneousFlashes and stepFlashesNumber == tilesNumber:
			return step
	return sumFlashesNumber


inputData = getFileContent('resources/input_11.txt')

grid = getGrid(inputData)
print('', *grid, '', sep='\n')

steps = 100
flashesNumber = run(grid, steps)
print('Flashes number after %d steps: %d\n' % (steps, flashesNumber)) # 1719

# ------------------------------------------
# Part 2:

grid = getGrid(inputData) # resetting the grid!

step = run(grid, -1, stopAtSimultaneousFlashes=True)
print('Simultaneous flashes at step: %d' % step) # 232
