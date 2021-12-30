import math

def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

# inputData = '''
# start-A
# start-b
# A-c
# A-b
# b-d
# A-end
# b-end
# '''.split('\n')

inputData = getFileLines('resources/input_12.txt')

entries = [ entry.split('-') for entry in inputData if entry != '' ]
print('entries:', entries)

def getNodes(entries):
	nodes = set()
	for entry in entries:
		nodes.add(entry[0])
		nodes.add(entry[1])
	return nodes

isSmallCave = lambda s : s != 'start' and s != 'end' and ord(s[0]) in range(ord('a'), ord('z')+1)

nodes = getNodes(entries)
print('\nNodes:', sorted(nodes))

smallCaves = set(filter(isSmallCave, nodes))
print('\nSmall caves:', sorted(smallCaves))

def getIncidenceMap(entries, nodes):
	incidenceMap = { node : set() for node in nodes }
	for entry in entries:
		node_1, node_2 = entry
		incidenceMap[node_1].add(node_2)
		incidenceMap[node_2].add(node_1)
	return incidenceMap

incidenceMap = getIncidenceMap(entries, nodes)
print('\nIncidence map:\n', *incidenceMap.items(), '', sep='\n')

class Path:
	def __init__(self):
		self.path = ['start']
		self.visitCounts = { 'start' : 1 }
		self.aSmallCaveTwiceVisited = False

	def print(self):
		print('Path:', self.path)
		print('Visited:', self.visitCounts)

	def copy(self):
		path = Path()
		path.path = self.path.copy()
		path.visitCounts = self.visitCounts.copy()
		path.aSmallCaveTwiceVisited = self.aSmallCaveTwiceVisited
		return path

	def add(self, node):
		self.path.append(node)
		if not node in self.visitCounts:
			self.visitCounts[node] = 0
		self.visitCounts[node] += 1
		if node in smallCaves and self.visitCounts[node] > 1:
			self.aSmallCaveTwiceVisited = True

def numberAllowedVisit(node, path, smallCaves):
	if node == 'start' or node == 'end' or node in smallCaves:
		return 1
	return math.inf

# Careful: a given path may never reach the end or be continued!
def findAllPaths(foundPaths, incidenceMap, path):
	for neighbor in incidenceMap[path.path[-1]]:
		if neighbor in path.visitCounts and path.visitCounts[neighbor] >= numberAllowedVisit(neighbor, path, smallCaves):
			continue
		newPath = path.copy()
		newPath.add(neighbor)
		if neighbor == 'end':
			foundPaths.append(newPath)
		else:
			findAllPaths(foundPaths, incidenceMap, newPath)

def printFoundPaths(foundPaths, verbose=False):
	if verbose:
		print('Found paths:\n')
		foundPaths = sorted([ path.path for path in foundPaths ])
		for path in foundPaths:
			print(','.join(path))
	print('\n%d paths found.\n' % len(foundPaths))


foundPaths = []
findAllPaths(foundPaths, incidenceMap, Path())
printFoundPaths(foundPaths, verbose=False) # 4970

# ------------------------------------------
# Part 2:

def numberAllowedVisit(node, path, smallCaves):
	if node == 'start' or node == 'end':
		return 1
	if node in smallCaves:
		return 1 if path.aSmallCaveTwiceVisited else 2
	return math.inf

foundPaths = []
findAllPaths(foundPaths, incidenceMap, Path())
printFoundPaths(foundPaths, verbose=False) # 137948 in 1.3s
