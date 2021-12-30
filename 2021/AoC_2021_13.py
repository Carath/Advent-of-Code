def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

def parseData(inputData):
	inputData = [ [ s for s in data.split('\n') if s != '' ] for data in inputData.split('\n\n') ]
	inputData = [ data for data in inputData if data != [] ]
	dots, instructions = inputData
	dots = [ dot.split(',') for dot in dots ]
	dots = [ [int(dot[0]), int(dot[1])] for dot in dots ]
	instructions = [ instr.split('fold along ')[1].split('=') for instr in instructions ]
	instructions = [ [instr[0], int(instr[1])] for instr in instructions ]
	return dots, instructions

# Careful! (x, y) <-> (col, row)

def getDimensions(dots):
	rowBound = max([ dot[1] for dot in dots ]) + 1
	colBound = max([ dot[0] for dot in dots ]) + 1
	return rowBound, colBound

def getGrid(dots):
	rowBound, colBound = getDimensions(dots)
	print('\nrowBound:', rowBound, ', colBound:', colBound)
	grid = [ ['.'] * colBound for row in range(rowBound) ]
	for dot in dots:
		col, row = dot
		grid[row][col] = '#'
	return grid

def printGrid(grid):
	print('', *[ ''.join(grid[row]) for row in range(len(grid)) ], '', sep='\n')

# Careful, grid changes of size!
def fold(grid, instructions):
	countAfterFirstFold = 0
	for instrIndex in range(len(instructions)):
		axis, val = instructions[instrIndex]
		if axis == 'x':
			dist = min(val, len(grid[0]) - 1 - val)
			for row in range(len(grid)):
				for i in range(1, dist+1):
					if grid[row][val + i] == '#':
						grid[row][val - i] = '#'
				grid[row] = grid[row][:val]
		if axis == 'y':
			dist = min(val, len(grid) - 1 - val)
			for i in range(1, dist+1):
				for col in range(len(grid[0])):
					if grid[val + i][col] == '#':
						grid[val - i][col] = '#'
			del grid[val:]
		if instrIndex == 0:
			for row in range(len(grid)):
				for col in range(len(grid[0])):
					countAfterFirstFold += int(grid[row][col] == '#')
	return countAfterFirstFold


inputData = getFileContent('resources/input_13.txt')
dots, instructions = parseData(inputData)
print('dots:', *dots, sep='\n')
print('\ninstructions:', *instructions, sep='\n')

grid = getGrid(dots)
# printGrid(grid)

countAfterFirstFold = fold(grid, instructions)
print('\nCount after first fold:', countAfterFirstFold) # 695

# ------------------------------------------
# Part 2:

printGrid(grid) # code: GJZGLUPJ
