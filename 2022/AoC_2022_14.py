def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_14.txt"
path = "resources/input_14.txt"

lines = [ line.split(" -> ") for line in getFileContent(path).split("\n") if line != "" ]
lines = [ [ [ int(x) for x in s.split(",") ] for s in line ] for line in lines ]
print(*lines, "", sep="\n")

maxRow = max(set([ coord[1] for line in lines for coord in line ]))
print("maxRow: %d\n" % maxRow)

source = 500
grid = [ ['.'] * (2*source) for i in range(maxRow+3) ]

def printGrid(grid, size=20):
	for i in range(len(grid)):
		print(''.join(grid[i][source-size:source+size]))
	print()

# Filling the grid:
for line in lines:
	for i in range(len(line)-1):
		deltaCol, deltaRow = line[i+1][0]-line[i][0], line[i+1][1]-line[i][1]
		deltaCol = deltaCol if deltaCol == 0 else deltaCol // abs(deltaCol)
		deltaRow = deltaRow if deltaRow == 0 else deltaRow // abs(deltaRow)
		coord = line[i][:]
		while coord != line[i+1]:
			grid[coord[1]][coord[0]] = '#'
			coord[0] += deltaCol
			coord[1] += deltaRow
		grid[line[i+1][1]][line[i+1][0]] = '#'

# printGrid(grid)

def sandFlow(grid):
	grid = [ row[:] for row in grid ] # faster than copy.deepcopy()
	sandNumber = 0
	while True:
		sandRow, sandCol = 0, source
		while sandRow < len(grid)-1:
			if grid[sandRow+1][sandCol] == '.':
				sandRow += 1
			elif grid[sandRow+1][sandCol-1] == '.':
				sandRow += 1
				sandCol -= 1
			elif grid[sandRow+1][sandCol+1] == '.':
				sandRow += 1
				sandCol += 1
			else:
				grid[sandRow][sandCol] = 'o' # becomes still
				sandNumber += 1
				break
		if sandRow >= len(grid)-1 or sandRow == 0:
			# printGrid(grid)
			return sandNumber

result = sandFlow(grid)
print("\nResult:", result, "\n") # 715

# # ------------------------------------------
# # Part 2:

for j in range(len(grid[-1])):
	grid[maxRow+2][j] = '#'

result = sandFlow(grid)
print("\nResult 2:", result) # 25248 in 0.7 s
