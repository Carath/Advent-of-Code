def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# inputData = getFileContent('resources/example_22.txt')
inputData = getFileContent('resources/input_22.txt')
inputData = [ s for s in inputData.split('\n') if s != '' ]
print('inputData:', *inputData, '', sep='\n')

def getRules(inputData):
	rules = []
	for entry in inputData:
		entry = entry.split(' ')
		status, cuboid = entry[0] == 'on', entry[1].split(',')
		for i in range(len(cuboid)):
			start = cuboid[i].index('=')
			cuboid[i] = cuboid[i][start+1:].split('..')
			cuboid[i] = [ int(aRange) for aRange in cuboid[i] ]
		rules.append((status, cuboid))
	return rules

rules = getRules(inputData)
print('\nRules:', *rules, '', sep='\n')

def cuboidsIntersection(cuboid_1, cuboid_2):
	return ((max(cuboid_1[0][0], cuboid_2[0][0]), min(cuboid_1[0][1], cuboid_2[0][1])),
			(max(cuboid_1[1][0], cuboid_2[1][0]), min(cuboid_1[1][1], cuboid_2[1][1])),
			(max(cuboid_1[2][0], cuboid_2[2][0]), min(cuboid_1[2][1], cuboid_2[2][1])))

def cuboidVolume(cuboid):
	if cuboid[0][0] <= cuboid[0][1] and cuboid[1][0] <= cuboid[1][1] and cuboid[2][0] <= cuboid[2][1]:
		return (cuboid[0][1] - cuboid[0][0] + 1) * (cuboid[1][1] - cuboid[1][0] + 1) * (cuboid[2][1] - cuboid[2][0] + 1)
	return 0

def cuboidCheck(cuboid, maxDistance=50):
	for aRange in cuboid:
		for value in aRange:
			if not value in range(-maxDistance, maxDistance+1):
				return False
	return True

def getRulesIntersection(rules, intersectingCuboid):
	rulesIntersection = []
	for rule in rules:
		status, cuboid = rule
		intersected = cuboidsIntersection(cuboid, intersectingCuboid)
		if cuboidVolume(intersected) > 0: # removing as much cuboids as possible!
			rulesIntersection.append((status, intersected))
	return rulesIntersection

def countActiveCubes(rules, onlyInitRegion=False):
	if rules == []:
		return 0
	status, cuboid, nextRules = *rules[-1], rules[:-1]
	count = countActiveCubes(nextRules, onlyInitRegion)
	if onlyInitRegion and not cuboidCheck(cuboid):
		return count
	count -= countActiveCubes(getRulesIntersection(nextRules, cuboid), onlyInitRegion)
	if status:
		count += cuboidVolume(cuboid)
	return count

activeCubes = countActiveCubes(rules, True)
print('\nActive cubes at init:', activeCubes) # 567496

# ------------------------------------------
# Part 2:

activeCubes = countActiveCubes(rules, False)
print('\nActive cubes:', activeCubes) # 1355961721298916 in 0.3s
