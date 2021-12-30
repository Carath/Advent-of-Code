# Implementations of Dijkstra's algorithm (uniform-cost search variant) for shortest path in a directed graph.
# Supported features:
# - Nodes can be any hashable type.
# - Directed edges with float weights (must be > 0).
# - Infinite graphs (early stopping if a target is reached) or unexplored graphs (nodes and edges are discovered dynamically).
# - Several target nodes, defined explicitely or by a predicate.
# - Algorithm will terminate correctly if the starting region is finite but no target nodes is reachable.

from queue import PriorityQueue

class DijkstraSearch:

	def __init__(self, getWeight, getNeighbors, isTarget):
		self.getWeight = getWeight
		self.getNeighbors = getNeighbors
		self.isTarget = isTarget

	# Using Python's 'PriorityQueue', no 'visited' set and no infinite distance.
	def dijkstra(self, graphData, start, targetData):
		pathMap = { start : (0, None) } # node -> (distance, previous node)
		pq = PriorityQueue()
		pq.put((0, start))
		while not pq.empty():
			(distClosest, closest) = pq.get()
			if self.isTarget(targetData, closest): # early stopping
				return distClosest, self.buildPath(pathMap, closest)
			neighbors = self.getNeighbors(graphData, closest)
			for neighbor in neighbors:
				newDist = distClosest + self.getWeight(graphData, closest, neighbor)
				if neighbor not in pathMap or newDist < pathMap[neighbor][0]:
					pq.put((newDist, neighbor))
					pathMap[neighbor] = (newDist, closest)
		return None, [] # target unreachable.

	# Implementing a priority queue structure, a bit like in Dial's algorithm
	# but supporting float weights. No infinite distance used.
	def dijkstra_homemade(self, graphData, start, targetData):
		pathMap = { start : (0, None) } # node -> (distance, previous node)
		distRings = { 0 : set([start]) } # distance -> nodes set
		foundDistances = [0] # must stay sorted
		while True:
			closest, keyIdx = None, 0
			while keyIdx < len(foundDistances):
				key = foundDistances[keyIdx]
				if distRings[key] != set():
					closest = list(distRings[key])[0]
					distClosest = key
					break
				keyIdx += 1
			if closest == None:
				return None, [] # target unreachable.
			if self.isTarget(targetData, closest): # early stopping
				return distClosest, self.buildPath(pathMap, closest)
			distRings[distClosest].remove(closest)
			foundDistances = foundDistances[keyIdx:]
			sortNeeded = False
			neighbors = self.getNeighbors(graphData, closest)
			for neighbor in neighbors:
				newDist = distClosest + self.getWeight(graphData, closest, neighbor)
				if neighbor not in pathMap or newDist < pathMap[neighbor][0]:
					if neighbor in pathMap:
						distRings[pathMap[neighbor][0]].remove(neighbor)
					if not newDist in distRings:
						distRings[newDist] = set()
						foundDistances.append(newDist)
						sortNeeded = True
					distRings[newDist].add(neighbor)
					pathMap[neighbor] = (newDist, closest)
			if sortNeeded:
				foundDistances.sort() # suboptimal, but Python's sort is quite fast on almost sorted lists!

	def buildPath(self, pathMap, foundTarget):
		if foundTarget == None:
			print('Impossible to build a path: no target reached!')
			return []
		path, curr = [], foundTarget
		while curr != None:
			path.append(curr)
			curr = pathMap[curr][1]
		path.reverse()
		return path


def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

def getGrid(string):
	grid = [ list(s) for s in string.split('\n') if s != '' ]
	return [ [ int(col) for col in row ] for row in grid ]

def isInGraph(grid, coord):
	return coord[0] in range(len(grid)) and coord[1] in range(len(grid[0]))

# Weights are only used between neighbors, and must be > 0:
def getWeight(graphData, source, dest):
	return graphData[dest[0]][dest[1]]

# Size 4 neighbourhood. Careful, neighbourhoods must _not_ contain their center cell!
def getNeighbors(graphData, node):
	neighbors = [(node[0]-1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1), (node[0]+1, node[1])]
	return [ c for c in neighbors if isInGraph(graphData, c) ]

# This can be a condition only checkable upon reaching the coord, e.g when the graph is discovered gradually.
# Here, 'targetData' is the target coord:
def isTarget(targetData, node):
	return node == targetData

def duplicateGrid(grid, count):
	newGrid = [ [0] * (count * len(grid[0])) for row in range(count * len(grid)) ]
	for rowChunk in range(count):
		for colChunk in range(count):
			offset = rowChunk + colChunk
			for row in range(len(grid)):
				for col in range(len(grid[row])):
					newValue = grid[row][col] + offset
					newValue = newValue if newValue < 10 else newValue - 9
					newGrid[rowChunk * len(grid) + row][colChunk * len(grid[row]) + col] = newValue
	return newGrid


if __name__ == '__main__':

	search = DijkstraSearch(getWeight, getNeighbors, isTarget)

	# inputData = getFileContent('resources/example_15.txt')
	inputData = getFileContent('resources/input_15.txt')

	grid = getGrid(inputData)
	start, end = (0, 0), (len(grid)-1, len(grid[0])-1)

	distance, path = search.dijkstra(grid, start, end)
	# distance, path = search.dijkstra_homemade(grid, start, end)

	print('\nPath:', path)
	print('\nDistance:', distance) # 714

	# ------------------------------------------
	# Part 2:

	newGrid = duplicateGrid(grid, count=5)
	# print('\nNew grid:', *newGrid, '', sep='\n')
	start, end = (0, 0), (len(newGrid)-1, len(newGrid[0])-1)

	distance, path = search.dijkstra(newGrid, start, end)
	# distance, path = search.dijkstra_homemade(newGrid, start, end)

	# print('\nPath:', path)
	print('\nDistance:', distance) # 2948 in 2.3s (1.7s with homemade version)
