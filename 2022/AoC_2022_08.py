def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_08.txt"
path = "resources/input_08.txt"

content = getFileContent(path)

grid = [ [ int(c) for c in line ] for line in content.split("\n") if line != "" ]
width, height = len(grid[0]), len(grid)
# print("", *grid, sep="\n")

limits = {}
for row in range(height):
	for col in range(width):
		rowMin, rowMax, colMin, colMax = row-1, row+1, col-1, col+1
		while rowMin >= 0 and grid[rowMin][col] < grid[row][col]: # top
			rowMin -= 1
		while rowMax < height and grid[rowMax][col] < grid[row][col]: # bottom
			rowMax += 1
		while colMin >= 0 and grid[row][colMin] < grid[row][col]: # left
			colMin -= 1
		while colMax < width and grid[row][colMax] < grid[row][col]: # right
			colMax += 1
		limits[(row, col)] = (rowMin, rowMax, colMin, colMax)

# print("limits:", *limits.items(), "", sep="\n")

isVisible = lambda limit : limit[0] < 0 or limit[1] >= height or limit[2] < 0 or limit[3] >= width

result = sum([ int(isVisible(value)) for value in limits.values() ])
print("\nResult:", result, "\n") # 1870

# # ------------------------------------------
# # Part 2:

def score(row, col, limit):
	return (row-max(0, limit[0])) * (min(height-1, limit[1])-row) * (col-max(0, limit[2])) * (min(width-1, limit[3])-col)

scores = sorted([ (c[0], score(c[0][0], c[0][1], c[1])) for c in limits.items() ], key=lambda c : c[1], reverse=True)
bestTree, bestScore = scores[0]
print("Best tree: %s, best score: %d" % (bestTree, bestScore))

print("\nResult 2:", bestScore) # 517440
