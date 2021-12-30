def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

def getTemplateAndRules(inputData):
	inputData = [ s for s in inputData.split('\n\n') if s != '' ]
	inputData = [ [ s for s in line.split('\n') if s != '' ] for line in inputData ]
	template = inputData[0][0]
	rules = [ s.split(' -> ') for s in inputData[1] ]
	return template, rules

def getRulesMap(rules):
	rulesMap = {}
	for rule in rules:
		pair, element = rule[0], rule[1]
		rulesMap[pair] = element
	return rulesMap

def evolve(template, rulesMap, steps):
	currentPolymer, elements = list(template), {}
	for step in range(steps):
		# print(''.join(currentPolymer))
		nextPolymer = [currentPolymer[0]]
		for i in range(len(currentPolymer)-1):
			pair = currentPolymer[i] + currentPolymer[i+1]
			if pair in rulesMap:
				nextPolymer.append(rulesMap[pair])
			nextPolymer.append(currentPolymer[i+1])
		currentPolymer = nextPolymer
	# print(''.join(currentPolymer))
	for c in currentPolymer:
		increment(elements, c)
	return elements

def increment(aDict, key):
	if not key in aDict:
		aDict[key] = 0
	aDict[key] += 1

def countElements(elements):
	elements = list(elements.items())
	elements.sort(key=lambda c : c[1])
	print('\nElements:', elements)
	return elements[-1][1] - elements[0][1]


# inputData = getFileContent('resources/example_14.txt')
inputData = getFileContent('resources/input_14.txt')

template, rules = getTemplateAndRules(inputData)
print('Template:', template, '\n\nRules:', rules)

rulesMap = getRulesMap(rules)
print('\nrulesMap:', rulesMap)

elements = evolve(template, rulesMap, 10)
result = countElements(elements)
print('\nResult:', result, '\n') # 2375

# ------------------------------------------
# Part 2:

def addCount(srcDict, destDict, oldKey, newKey):
	if not newKey in destDict:
		destDict[newKey] = 0
	destDict[newKey] += srcDict[oldKey]

def evolveFast(template, rulesMap, steps):
	pairsList = [ template[i]+template[i+1] for i in range(len(template)-1) ]
	pairs, elements = {}, {}
	for pair in pairsList:
		increment(pairs, pair)
	for step in range(steps):
		nextPairs = {}
		for pair in pairs:
			if pair in rulesMap:
				addCount(pairs, nextPairs, pair, pair[0] + rulesMap[pair])
				addCount(pairs, nextPairs, pair, rulesMap[pair] + pair[1])
			else:
				addCount(pairs, nextPairs, pair, pair)
		pairs = nextPairs
	for pair in pairs:
		addCount(pairs, elements, pair, pair[0])
	elements[template[-1]] += 1 # last element is missing.
	return elements

elements = evolveFast(template, rulesMap, 40)
result = countElements(elements)
print('\nResult:', result) # 1976896901756
