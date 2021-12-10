from tqdm import tqdm
from AoC_2019_09 import *

def fillGrid(program, size):
	grid = [ ['.'] * size for i in range(size) ]
	for row in range(0, size):
		for col in range(0, size):
			outputs = run(program, [col, row])[0]
			if outputs[0] == 1:
				grid[row][col] = '#'
	return grid

def printGrid(grid):
	print()
	for i in range(len(grid)):
		print(''.join(grid[i]))
	print()

def countGridBeam(grid):
	count = 0
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == '#':
				count += 1
	return count


inputFile = 'resources/input_19.txt'
stringInput = getFileLines(inputFile)[0]
print(stringInput, '\n')
program = getInput(stringInput)
program += [0] * 1000

size = 50
grid = fillGrid(program, size)
printGrid(grid)

theCount = countGridBeam(grid)
print('Count:', theCount, '\n') # 220 (in 10 sec)

# ------------------------------------------
# Part 2:

def getBounds(rowMax, maxSearchDist):
	bounds, lastMinCol, lastMaxCol = [], 0, 0
	for row in tqdm(range(rowMax)):
		rowBounds, statusSndBound = [], False
		for col in range(lastMinCol, lastMinCol + maxSearchDist):
			outputs = run(program, [col, row])[0]
			if outputs[0] == 1:
				lastMinCol = col
				rowBounds.append(col)
				break
		for col in range(lastMaxCol, lastMaxCol + maxSearchDist):
			outputs = run(program, [col, row])[0]
			if outputs[0] == 1:
				statusSndBound = True
				lastMaxCol = col
			elif statusSndBound:
				rowBounds.append(col - 1)
				break
		bounds.append(rowBounds)
	return bounds

def findSquarePos(bounds, squareLength):
	for row in range(squareLength - 1, len(bounds)):
		aboveRow = row - squareLength + 1
		if bounds[row] == [] or bounds[aboveRow] == []:
			continue
		currColStart = bounds[row][0]
		aboveColEnd = bounds[aboveRow][1]
		if aboveColEnd - currColStart >= squareLength - 1:
			print('Found! top left row, col: (%d, %d)' % (aboveRow, currColStart))
			return aboveRow, currColStart
	if row == len(bounds) - 1:
		print('Not found!')
	return -1, -1


bounds = getBounds(1000, maxSearchDist=10)
# print('\nbounds:', *bounds, sep='\n')

squareLength = 100
aboveRow, currColStart = findSquarePos(bounds, squareLength)
result = currColStart * 10000 + aboveRow
print('\nResult:', result) # 10010825
