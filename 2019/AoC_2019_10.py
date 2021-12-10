import math

example = 'resources/example_10.txt'
theinput = 'resources/input_10.txt'
data = theinput

def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

lines = getFileLines(data)
print('', *lines, '', sep='\n')

def buildMatrix(lines):
	asteroids = set()
	matrix = [0] * len(lines)
	for row in range(len(lines)):
		matrix[row] = [''] * len(lines[row])
		for col in range(len(lines[row])):
			matrix[row][col] = lines[row][col]
			if lines[row][col] == '#':
				asteroids.add((row, col))
	return matrix, asteroids

matrix, asteroids = buildMatrix(lines)
print('', *matrix, '', sep='\n')
print('asteroids:', asteroids)

def convertToCoord(point):
	return point[1], point[0]

def isInGrid(point, matrix):
	return 0 <= point[0] and point[0] < len(matrix) and 0 <= point[1] and point[1] < len(matrix[0])

def gcd(a, b): # a, b >= 0
	if b == 0:
		return a
	else:
		return gcd(b, a % b)

def computeDirections(matrix):
	directions = set()
	for dirRow in range(len(matrix) + 1):
		for dirCol in range(len(matrix[0]) + 1):
			if gcd(dirRow, dirCol) == 1:
				directions.add((dirRow, dirCol))
				directions.add((-dirRow, dirCol))
				directions.add((dirRow, -dirCol))
				directions.add((-dirRow, -dirCol))
	return directions

directions = computeDirections(matrix)
# print('\ndirections:', directions)

def computeVisiblesPoint(ref, matrix, asteroids, directions):
	visiblesCount = 0
	for direc in directions:
		curr = ref
		while isInGrid(curr, matrix) and (curr == ref or not curr in asteroids):
			curr = (curr[0] + direc[0], curr[1] + direc[1])
		if curr in asteroids:
			visiblesCount += 1
	return visiblesCount

def findBestSpot(matrix, asteroids, directions):
	bestSpot, bestCount = 0, 0
	for spot in asteroids:
		count = computeVisiblesPoint(spot, matrix, asteroids, directions)
		if count > bestCount:
			bestCount = count
			bestSpot = spot
	return bestSpot, bestCount

bestSpot, bestCount = findBestSpot(matrix, asteroids, directions)
print('\n-> Best spot:', convertToCoord(bestSpot), 'with count:', bestCount)

# ------------------------------------------
# Part 2:

# Careful: (row, col) <-> (y, x)

heaviside = lambda x : 1 if x >= 0 else -1
norm = lambda x, y: math.sqrt(x * x + y * y)
orderKey = lambda x, y : (-heaviside(y), heaviside(y) * x / norm(x, y))

sortedDirections = sorted(directions, key=lambda point : orderKey(*point))
print('\nsortedDirections:', sortedDirections[:100], '...')

def findNthDestroyed(ref, matrix, asteroids, directions, rank):
	asteroidsLeft = asteroids.copy()
	destroyed = 0
	while True:
		for direc in directions:
			curr = ref
			while isInGrid(curr, matrix) and (curr == ref or not curr in asteroidsLeft):
				curr = (curr[0] + direc[0], curr[1] + direc[1])
			if curr in asteroidsLeft:
				asteroidsLeft.remove(curr)
				destroyed += 1
				if destroyed == rank:
					return curr

nth = findNthDestroyed(bestSpot, matrix, asteroids, sortedDirections, 200)
print('\n200th destroyed:', nth)
print('Answer:', nth[1] * 100 + nth[0])
