def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

inputData = getFileLines('resources/input_05.txt')
inputData = [ s.split(' -> ') for s in inputData if s != '']
inputData = [ [ col.split(',') for col in row ] for row in inputData ]
inputData = [ [ [ int(c) for c in col ] for col in row ] for row in inputData ]
print(*inputData, sep='\n')

def printGrid(grid):
	print()
	for row in grid:
		print(''.join(map(lambda k : '.' if k == 0 else str(k), row)))
	print()

def sgn(x):
	if x < 0:
		return -1
	if x == 0:
		return 0
	else:
		return 1

def fillGrid(data, noDiagonal):
	# Computing the grid size:
	gridSize = 0
	for d in data:
		gridSize = max(gridSize, d[0][0], d[0][1], d[1][0], d[1][1])
	gridSize += 1
	print('\ngrid size:', gridSize)
	# Filling the grid:
	grid = [ [0] * gridSize for row in range(gridSize)]
	for d in data:
		start, end = d[0], d[1]
		deltaX = sgn(end[0] - start[0])
		deltaY = sgn(end[1] - start[1])
		if noDiagonal and deltaX != 0 and deltaY != 0:
			# print('Skipping data:', d)
			continue
		curr = start[:]
		grid[curr[1]][curr[0]] += 1
		while curr != end:
			curr[0] += deltaX
			curr[1] += deltaY
			grid[curr[1]][curr[0]] += 1
	return grid

def countIntersections(grid):
	s = 0
	for row in grid:
		for col in row:
			if col >= 2:
				s += 1
	return s


grid = fillGrid(inputData, noDiagonal=True)
# printGrid(grid)

result = countIntersections(grid)
print('Result:', result) # 5092

# ------------------------------------------
# Part 2:

grid = fillGrid(inputData, noDiagonal=False)
# printGrid(grid)

result = countIntersections(grid)
print('Result:', result, '\n') # 20484
