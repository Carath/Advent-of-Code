def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# inputData = '''
# v...>>.vv>
# .vv>>.vv..
# >>.>v>...v
# >>v>>.>.v.
# v>v.vv.v..
# >.>>..v...
# .vv..>.>v.
# v.v..>>v.v
# ....v..v.>
# '''

inputData = getFileContent('resources/input_25.txt')

grid = [ list(s) for s in inputData.split('\n') if s != '' ]

def printGrid(grid, title=''):
	print(title, *[ ''.join(row) for row in grid ], '', sep='\n')

def run(grid, verbose=True):
	step = 0
	printGrid(grid, title='grid at step %d:' % step)
	while True:
		status = False
		# East facing ones move first:
		newGrid = [ row[:] for row in grid ] # copy to prevent side-effects
		for row in range(len(grid)):
			for col in range(len(grid[row])):
				char = grid[row][col]
				nextCol = (col+1) % len(grid[row])
				if char == '>' and grid[row][nextCol] == '.':
					newGrid[row][col] = '.'
					newGrid[row][nextCol] = char
					status = True
		grid = newGrid
		# Then south facing ones move:
		newGrid = [ row[:] for row in grid ] # copy to prevent side-effects
		for row in range(len(grid)):
			for col in range(len(grid[row])):
				char = grid[row][col]
				nextRow = (row+1) % len(grid)
				if char == 'v' and grid[nextRow][col] == '.':
					newGrid[row][col] = '.'
					newGrid[nextRow][col] = char
					status = True
		grid = newGrid
		step += 1
		if verbose:
			printGrid(grid, title='grid at step %d:' % step)
		if not status:
			return step

step = run(grid, verbose=True)
print('Result:', step)
