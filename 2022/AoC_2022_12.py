import sys
sys.path.insert(0, '../2021/')
from AoC_2021_15 import DijkstraSearch

def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_12.txt"
path = "resources/input_12.txt"

grid = [ [ ord(c) for c in s ] for s in getFileContent(path).split("\n") if s != "" ]
# print("grid:", *grid, "", sep="\n")

start, end = (0, 0), (0, 0)
for row in range(len(grid)):
	for col in range(len(grid[0])):
		if grid[row][col] == ord('S'):
			start = (row, col)
		elif grid[row][col] == ord('E'):
			end = (row, col)
print("Start: %s, end: %s" % (start, end))

# Replacing starting and ending positions by their elevation:
grid[start[0]][start[1]] = ord('a')
grid[end[0]][end[1]] = ord('z')

def getWeight(graphData, source, dest):
	return 1

def isInGraph(grid, coord):
	return coord[0] in range(len(grid)) and coord[1] in range(len(grid[0]))

neighbors = lambda node : [(node[0]-1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1), (node[0]+1, node[1])]

def getNeighbors(graphData, node):
	return [ c for c in neighbors(node) if isInGraph(graphData, c) and grid[c[0]][c[1]] <= grid[node[0]][node[1]]+1 ]

def isTarget(targetData, node):
	return node == targetData # Do not stop at any ord('z'), we want to reach the real 'E'.

search = DijkstraSearch(getWeight, getNeighbors, isTarget)

distance, path = search.dijkstra_homemade(grid, start, end)

# print('\nPath:', path)
print('\nDistance:', distance)

result = distance
print("\nResult:", result, "\n") # 425

# # ------------------------------------------
# # Part 2:

# Running the search from the end:

def isTarget_rev(targetData, node):
	return grid[node[0]][node[1]] == ord('a')

def getNeighbors_rev(graphData, node):
	return [ c for c in neighbors(node) if isInGraph(graphData, c) and grid[c[0]][c[1]] >= grid[node[0]][node[1]]-1 ]

search = DijkstraSearch(getWeight, getNeighbors_rev, isTarget_rev)

distance, path = search.dijkstra_homemade(grid, end, None) # reversed path
print('\nBest distance:', distance)

result = distance
print("\nResult 2:", result) # 418

# Total time: 66 ms
