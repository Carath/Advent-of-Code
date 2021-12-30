from math import cos, sin, pi

def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# inputData = getFileContent('resources/example_19.txt')
inputData = getFileContent('resources/input_19.txt')

def getScannersData(inputData):
	scannersData = {}
	inputData = inputData.split('\n\n')
	for scannerIdx in range(len(inputData)):
		scannersData[scannerIdx] = set()
		data = inputData[scannerIdx].split('\n')[1:]
		data = [ s for s in data if s != '']
		for entry in data:
			entry = [ int(s) for s in entry.split(',') ]
			scannersData[scannerIdx].add(tuple(entry))
	return scannersData

scannersData = getScannersData(inputData)
# print(*scannersData.items(), sep='\n\n')

scanners = sorted(scannersData.keys())

def rot_xy(theta):
	return [[cos(theta), -sin(theta), 0],
			[sin(theta), cos(theta), 0],
			[0, 0, 1]]

def rot_xz(theta):
	return [[cos(theta), 0, -sin(theta)],
			[0, 1, 0],
			[sin(theta), 0, cos(theta)]]

def rot_yz(theta):
	return [[1, 0, 0],
			[0, cos(theta), -sin(theta)],
			[0, sin(theta), cos(theta)]]

def matrixProduct(matrix_1, matrix_2):
	if len(matrix_1[0]) != len(matrix_2):
		print('\nMatrix product failure: incompatible sizes: %d vs %d' % (len(matrix_1[0]), len(matrix_2)))
		exit()
	matrix = [ [0] * len(matrix_2[0]) for i in range(len(matrix_1)) ]
	for i in range(len(matrix_1)):
		for j in range(len(matrix_2[0])):
			for k in range(len(matrix_2)):
				matrix[i][j] += matrix_1[i][k] * matrix_2[k][j]
	return matrix

def buildRotationMatrices():
	rotationMatrices_1, rotationMatrices_2, rotationMatrices = [], [], []
	for theta in [0, pi/2, pi, -pi/2]:
		rotationMatrices_1.append(rot_xy(theta))
	for theta in [pi/2, -pi/2]:
		rotationMatrices_1.append(rot_xz(theta))
	for theta in [0, pi/2, pi, -pi/2]:
		rotationMatrices_2.append(rot_yz(theta))
	for matrix_1 in rotationMatrices_1:
		for matrix_2 in rotationMatrices_2:
			matrix = matrixProduct(matrix_1, matrix_2)
			for i in range(len(matrix)):
				matrix[i] = [ int(val) for val in matrix[i] ]
			rotationMatrices.append(matrix)
	return rotationMatrices

rotationMatrices = buildRotationMatrices()

for matrix in rotationMatrices:
	print('', *matrix, sep='\n')

def buildInverseMap(rotationMatrices):
	inverseMap = {}
	identityMatrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
	for i in range(len(rotationMatrices)):
		if i in inverseMap: # already found by symmetry!
			continue
		for j in range(i, len(rotationMatrices)):
			if matrixProduct(rotationMatrices[i], rotationMatrices[j]) == identityMatrix:
				inverseMap[i] = j
				inverseMap[j] = i
				break
	return inverseMap

inverseMap = buildInverseMap(rotationMatrices)
print('\ninverseMap:', sorted(inverseMap.items()), '\n')

# Rotating with origin 0, which is chosen to be the first scanner:
def rotate(rotationMatrices, matrixIdx, point):
	vector = [ [point[0]], [point[1]], [point[2]] ]
	rotated = matrixProduct(rotationMatrices[matrixIdx], vector)
	return (rotated[0][0], rotated[1][0], rotated[2][0])

# Precomputed rotations on each clusters:
def buildAllPossibilities(scannersData, rotationMatrices):
	possibilities = {}
	for scannerIdx in scannersData:
		if scannerIdx == 0: # First scanner taken as reference.
			possibilities[0] = {0 : scannersData[0]}
			continue
		possibilities[scannerIdx] = {}
		for matrixIdx in range(len(rotationMatrices)):
			possibilitySet = set()
			possibilities[scannerIdx][matrixIdx] = possibilitySet
			for data in scannersData[scannerIdx]:
				possibilitySet.add(rotate(rotationMatrices, matrixIdx, data))
	return possibilities

possibilities = buildAllPossibilities(scannersData, rotationMatrices)
# print('', *possibilities[1].items(), '', sep='\n\n')

def manhattanDistance(point_1, point_2):
	return abs(point_1[0]-point_2[0]) + abs(point_1[1]-point_2[1]) + abs(point_1[2]-point_2[2])

def computeDistancePatterns(scanners, scannersData):
	intraClusterDistances = { key : set() for key in scanners }
	distancesToEdges = { key : {} for key in scanners }
	for key in scanners:
		dataList = list(scannersData[key])
		for i in range(len(dataList)):
			for j in range(i+1, len(dataList)):
				data_1, data_2 = dataList[i], dataList[j]
				distance = manhattanDistance(data_1, data_2)
				intraClusterDistances[key].add(distance)
				distancesToEdges[key][distance] = (data_1, data_2)
	return intraClusterDistances, distancesToEdges

intraClusterDistances, distancesToEdges = computeDistancePatterns(scanners, scannersData)

minMatchNumber = 12 # problem parameter

def validateRotationAndShift(possibilities, scanner_1, scanner_2, matrixIdx, shift):
	refSet = possibilities[scanner_1][0] # taken as reference
	possibility, count = possibilities[scanner_2][matrixIdx], 0
	for point in possibility:
		if (point[0]+shift[0], point[1]+shift[1], point[2]+shift[2]) in refSet:
			count += 1
			if count >= minMatchNumber:
				print('Found matches between scanners %d and %d!' % (scanner_1, scanner_2))
				print('  ... with matrixIdx: %d and shift:' % matrixIdx, shift)
				return True
	return False

# Trying every rotations by finding a pair of points giving matches:
def tryMatchingScanners_bruteForce(possibilities, scanner_1, scanner_2):
	refSet = possibilities[scanner_1][0] # taken as reference
	challengerDict = possibilities[scanner_2]
	for matrixIdx in challengerDict:
		possibility = challengerDict[matrixIdx]
		for a in refSet:
			for b in possibility:
				shift = (a[0]-b[0], a[1]-b[1], a[2]-b[2])
				if validateRotationAndShift(possibilities, scanner_1, scanner_2, matrixIdx, shift):
					return True, matrixIdx, shift
	return False, -1, None

def tryMatchingScanners_fast(possibilities, scanner_1, scanner_2):
	patternMatching = intraClusterDistances[scanner_1].intersection(intraClusterDistances[scanner_2])
	if len(patternMatching) >= minMatchNumber * (minMatchNumber-1) // 2:
		for aMatchingDist in patternMatching: # Careful to false positives!
			edge_1 = distancesToEdges[scanner_1][aMatchingDist]
			edge_2 = distancesToEdges[scanner_2][aMatchingDist]
			ref, candidate_1, candidate_2 = edge_1[0], edge_2[0], edge_2[1]
			challengerDict = possibilities[scanner_2]
			for matrixIdx in challengerDict:
				for candidate in [candidate_1, candidate_2]:
					candidate = rotate(rotationMatrices, matrixIdx, candidate)
					shift = (ref[0]-candidate[0], ref[1]-candidate[1], ref[2]-candidate[2])
					if validateRotationAndShift(possibilities, scanner_1, scanner_2, matrixIdx, shift):
						return True, matrixIdx, shift
	return False, -1, None

def findMatches(scanners, possibilities):
	matches = { key : {} for key in scanners }
	for scanner_1 in scanners:
		for scanner_2 in range(scanner_1+1, len(scanners)):
			# status, matrixIdx, shift = tryMatchingScanners_bruteForce(possibilities, scanner_1, scanner_2)
			status, matrixIdx, shift = tryMatchingScanners_fast(possibilities, scanner_1, scanner_2)
			if status:
				matches[scanner_1][scanner_2] = (matrixIdx, shift, True) # operator inverse!
				matches[scanner_2][scanner_1] = (matrixIdx, shift, False)
	return matches

matches = findMatches(scannersData, possibilities)
print('\nMatches:', *matches.items(), '', sep='\n')

def visit(visited, currentKey):
	for key in matches[currentKey]:
		if not key in visited:
			visited[key] = [matches[key][currentKey]] + visited[currentKey][:]
			visit(visited, key)

visited = { 0 : [] }
visit(visited, 0)
print('Visited:', *visited.items(), sep='\n')

def buildBeaconSet(scannersData, visited, inverseMap):
	beaconSet = set()
	scannersPosition = { key : (0, 0, 0) for key in visited }
	beaconsPerScanner = { key : [] for key in visited }
	for key in visited:
		scannersPosition[key] = applyOperators(inverseMap, visited[key], (0, 0, 0))
		for data in scannersData[key]:
			data = applyOperators(inverseMap, visited[key], data)
			beaconSet.add(data)
			beaconsPerScanner[key].append(data)
		beaconsPerScanner[key].sort()
	# print('\nbeaconsPerScanner:', *beaconsPerScanner.items(), sep='\n\n')
	print('\nscannersPosition:', *scannersPosition.items(), sep='\n')
	return beaconSet, scannersPosition

def applyOperators(inverseMap, operators, point):
	for operator in operators:
		matrixIdx, shift, inversed = operator
		if inversed:
			point = (point[0]-shift[0], point[1]-shift[1], point[2]-shift[2])
			point = rotate(rotationMatrices, inverseMap[matrixIdx], point)
		else:
			point = rotate(rotationMatrices, matrixIdx, point)
			point = (point[0]+shift[0], point[1]+shift[1], point[2]+shift[2])
	return point

beaconSet, scannersPosition = buildBeaconSet(scannersData, visited, inverseMap)
print('\nBeacons number:', len(beaconSet)) # 367

# ------------------------------------------
# Part 2:

def findLargestDistance(scanners, scannersPosition):
	largestDistance = 0
	for scanner_1 in scanners:
		for scanner_2 in range(scanner_1+1, len(scanners)):
			distance = manhattanDistance(scannersPosition[scanner_1], scannersPosition[scanner_2])
			if distance > largestDistance:
				largestDistance = distance
	return largestDistance

largestDistance = findLargestDistance(scanners, scannersPosition)
print('\nLargest distance:', largestDistance) # 11925 in 0.15s
