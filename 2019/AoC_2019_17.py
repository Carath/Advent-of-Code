from AoC_2019_09 import *

inputFile = 'resources/input_17.txt'
stringInput = getFileLines(inputFile)[0]
# print(stringInput, '\n')

program = getInput(stringInput)
program += [0] * 1000000

answer = run(program, [])
outputs, newProg = answer[0], answer[1]
# print('Outputs:', outputs)

# gridString = '''
# ..#..........
# ..#..........
# #######...###
# #.#...#...#.#
# #############
# ..#...#...#..
# ..#####...^..
# '''

# gridString = '''
# #######...#####
# #.....#...#...#
# #.....#...#...#
# ......#...#...#
# ......#...###.#
# ......#.....#.#
# ^########...#.#
# ......#.#...#.#
# ......#########
# ........#...#..
# ....#########..
# ....#...#......
# ....#...#......
# ....#...#......
# ....#####......
# '''

gridString = ''.join([ chr(value) for value in outputs])

print(gridString)

grid = list(filter(lambda s : s != '', gridString.split('\n')))
# print(*grid, sep='\n')

isInGrid = lambda coord : coord[0] in range(len(grid)) and coord[1] in range(len(grid[0]))

isScaffold = lambda coord : isInGrid(coord) and grid[coord[0]][coord[1]] == '#'

def neighbourhood(row, col):
	neighbors = [(row-1, col), (row, col-1), (row, col+1), (row+1, col)]
	return list(filter(isScaffold, neighbors))

def findIntersections(grid):
	intersections = []
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			if isScaffold((row, col)):
				neighbors = neighbourhood(row, col)
				if len(neighbors) == 4:
					intersections.append((row, col))
	return intersections

def getSumAlignParams(intersections):
	sumAlignParams = 0
	for coord in intersections:
		sumAlignParams += coord[0] * coord[1]
	return sumAlignParams


intersections = findIntersections(grid)
print('Intersections:', intersections)

sumAlignParams = getSumAlignParams(intersections)
print('\nResult:', sumAlignParams, '\n\n') # 12512

# ------------------------------------------
# Part 2:

isRobot = lambda coord : isInGrid(coord) and grid[coord[0]][coord[1]] in ['>', '<', '^', 'v']

def findStart(grid):
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			if isRobot((row, col)):
				return (row, col)
	print('Robot not found!')
	exit()

def getRobotDirection(coord):
	initChar = grid[coord[0]][coord[1]]
	print('Robot:', initChar)
	if initChar == '>':
		return (0, 1)
	elif initChar == '<':
		return (0, -1)
	elif initChar == '^':
		return (-1, 0)
	else: # 'v'
		return (1, 0)

getDirection = lambda src, dest : (dest[0] - src[0], dest[1] - src[1])

# Note: robot cannot look backward to the correct direction!
def computeTurn(currDirection, nextDirection):
	if currDirection == nextDirection:
		return '' # forward
	if nextDirection == (-currDirection[1], currDirection[0]): # Pi/2 rotation
		return 'L'
	return 'R'

def buildSegment(grid, startPos, direction):
	# print('Departing:', startPos, 'with direction:', direction)
	lastPos, coord, subpathLength = startPos, startPos, 0
	while True:
		newCoord = (coord[0] + direction[0], coord[1] + direction[1])
		if not isScaffold(newCoord):
			break
		lastPos, coord, subpathLength = coord, newCoord, subpathLength + 1
	# print('Stop!', coord, ', len:', subpathLength)
	neighbors = neighbourhood(*coord)
	candidates = list(filter(lambda coord : coord != lastPos, neighbors))
	if candidates == []:
		print('End reached!')
		return coord, (0, 0), '', subpathLength
	nextDirection = getDirection(coord, candidates[0])
	newTurn = computeTurn(direction, nextDirection)
	return coord, nextDirection, newTurn, subpathLength

# Careful! length may be 0, and turn may be ''
def buildPath(grid, initPos, initDirection):
	startPos, currDirection = initPos, initDirection
	path, subpathLength = [], 0
	while currDirection != (0, 0):
		startPos, currDirection, newTurn, subpathLength = buildSegment(grid, startPos, currDirection)
		path.append((subpathLength, newTurn))
	return path

def flattenPath(path):
	values = []
	for step in path:
		length, turn = step
		if length > 0:
			values.append(length)
		if turn != '':
			values.append(turn)
	return values

def countAppearances(sequence, chunks):
	count, anchors, newChunks = 0, [], []
	for chunkIndex in range(len(chunks)):
		chunkOffset, chunk = chunks[chunkIndex]
		i, lastIndex = 0, 0
		while i <= len(chunk) - len(sequence):
			if chunk[i : i + len(sequence)] == sequence:
				anchors.append((chunkIndex, i))
				newChunks.append((chunkOffset+lastIndex, chunk[lastIndex : i]))
				lastIndex = i + len(sequence)
				i = lastIndex
				count += 1
			else:
				i += 1
		newChunks.append((chunkOffset+lastIndex, chunk[lastIndex :])) # last new chunk!
	newChunks = list(filter(lambda c : c[1] != [], newChunks))
	return count, anchors, newChunks

# Finds at most 'depth' subsequences of a given list whose repeats yield said list:
def buildSolutionsTree(findings, chunks, maxSize, depth, sumCount=0, forceRepeat=False):
	if depth <= 0 or chunks == []:
		return chunks == [] and sumCount <= maxSize
	status, firstChunk = False, chunks[0][1]
	for size in range(min(maxSize, len(firstChunk)), 0, -1):
		sequence = firstChunk[:size]
		count, anchors, newChunks = countAppearances(sequence, chunks)
		newFindings = {}
		if not forceRepeat or count > 1:
			if buildSolutionsTree(newFindings, newChunks, maxSize, depth-1, sumCount+count, forceRepeat):
				findings[size] = {
					'count': count,
					'sequence': sequence,
					'chunks': newChunks,
					'anchors': anchors,
					'results': newFindings
				}
				status = True
	return status

def getASolution(aSolution, findings, chunks, names):
	keys = list(findings.keys())
	if keys == []:
		aSolution[0].sort()
		aSolution[0] = [ c[1] for c in aSolution[0] ]
		return
	firstFinding = findings[keys[0]]
	for anchor in firstFinding['anchors']:
		chunkIndex, i = anchor
		chunkOffset = chunks[chunkIndex][0]
		aSolution[0].append((chunkOffset + i, names[0]))
	aSolution.append(firstFinding['sequence'])
	getASolution(aSolution, firstFinding['results'], firstFinding['chunks'], names[1:])

# Enabling feedback slows things down!
def formatSolution(rules, feedback=False):
	rules = [ [ str(val) for val in rule ] for rule in rules ]
	rules = [ ','.join(rule) for rule in rules ]
	rules = '\n'.join(rules) + '\n%s\n' % ('y' if feedback else 'n')
	print("\nRules:\n'%s'" % rules)
	return [ ord(char) for char in rules ]


start = findStart(grid)
# print('Start:', start, '\n')

robotDirection = getRobotDirection(start)

path = buildPath(grid, start, robotDirection)
# print('\npath:', path)

flatPath = flattenPath(path)
print('\nPath formatted:', flatPath)

findings = {}
initChunks = [(0, flatPath)]
buildSolutionsTree(findings, initChunks, 10, 3) # 10 + 9 < 20
print('\n\nFindings:', *findings.items(), '', sep='\n\n')

aSolution = [[]]
getASolution(aSolution, findings, initChunks, ['A', 'B', 'C'])
print('A solution:', aSolution)

instructions = formatSolution(aSolution)
print('\nInstructions:', instructions)

program[0] = 2 # waking up the robot.
answer = run(program, instructions)

print('\nResult:', answer[0][-1]) # 1409507
