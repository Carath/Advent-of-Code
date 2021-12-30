def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

instructions = getFileLines('resources/input_24.txt')
# print('instructions:', *instructions, '', sep='\n')

def getInstructionsChunks(instructions):
	instructionsChunks = []
	start, curr = 0, 0
	for instr in instructions:
		if curr > 0 and instr.split(' ')[0] == 'inp':
			instructionsChunks.append(instructions[start : curr])
			start = curr
		curr += 1
	instructionsChunks.append(instructions[start:])
	return instructionsChunks

instructionsChunks = getInstructionsChunks(instructions)
print('instructions chunks:', *instructionsChunks, '', sep='\n')

# Only fetching relevant values. This may be input specific:
def getInstructionValues(instruction):
	a = int(instruction[3].split(' ')[-1]) # here a = 26
	b = int(instruction[4].split(' ')[-1]) # here b = 1 or 26
	c = int(instruction[5].split(' ')[-1])
	d = int(instruction[-3].split(' ')[-1]) # here 0 <= d <= 16
	# print('a: %d, b: %d, c: %d, d: %d' % (a, b, c, d))
	assert b in [1, a], "Not handled value of 'b': %d" % b
	assert d in range(a-9), "Not handled value of 'd': %d" % d
	return (a, b, c, d)

cleanedInstrChunks = [ getInstructionValues(instruction) for instruction in instructionsChunks ]
print('Cleaned instruction chunks:', *cleanedInstrChunks, '', sep='\n')

# This has been handcrafted based on features from the given input.
# It may not work on other inputs with different structure...
# Basically, given a z1 >= 0 this finds all (z0, w) with z0 >= 0 and 1 <= w <= 9 such that:
# z1 = (z0 // b) * ((a-1) * x + 1) + (w + d) * x where x = int(w != (z0 % a) + c).
def findInputsZandW(cleanedInstruction, z1):
	a, b, c, d = cleanedInstruction
	wRange, pairs = range(1, 10), []
	if b == 1:
		z0, w = z1, z1 % a + c
		if w in wRange:
			pairs.append((z0, w))
		z0, w = z1 // a, z1 % a - d
		if w in wRange and w != z0 % a + c:
			pairs.append((z0, w))
	else: # b == a
		for t in range(max(0, 1-c), min(a, 10-c)):
			z0, w = a * z1 + t, t + c # no need to test w range here!
			pairs.append((z0, w))
		for t in range(max(0, z1-a+1), z1+a):
			z0, w = t, z1 - t + t % a - d
			if w in wRange and w != t % a + c:
				pairs.append((z0, w))
	return pairs

# Tree is built from the end result by memoization of preimages. Produced results all are valid solutions.
def buildSolutionTree(solutions, cleanedInstrChunks, chunkIndex=len(cleanedInstrChunks)-1, z1=0):
	if chunkIndex < 0:
		return
	if chunkIndex not in solutions:
		solutions[chunkIndex] = {}
	if z1 not in solutions[chunkIndex]:
		solutions[chunkIndex][z1] = findInputsZandW(cleanedInstrChunks[chunkIndex], z1)
		for pair in solutions[chunkIndex][z1]:
			buildSolutionTree(solutions, cleanedInstrChunks, chunkIndex-1, pair[0])

def buildBestSolution(solutions, maximizing=True):
	multiplier, defaultBestDigit = (1, -1) if maximizing else (-1, 10)
	bestDigits, bestZset = [], set([0]) # init states must be 0
	indexes = sorted(solutions.keys())
	for chunkIndex in indexes:
		newBestZSet, bestDigit = set(), defaultBestDigit
		for z1 in solutions[chunkIndex]:
			for pair in solutions[chunkIndex][z1]:
				# Must fetch all z1 yielding to the best digit:
				z0, w = pair
				if z0 in bestZset and multiplier * (w - bestDigit) > 0:
					bestDigit = w
					newBestZSet = set([z1])
				elif z0 in bestZset and w == bestDigit:
					newBestZSet.add(z1)
		bestDigits.append(bestDigit)
		bestZset = newBestZSet
		print('rank: %2d, w: %d, next z:' % (chunkIndex, bestDigit), bestZset)
		if bestZset == set():
			print('\nFailed to build the best solution!')
			return []
	return bestDigits

def numberFromList(digits, radix=10):
	s, m = 0, 1
	for i in range(len(digits)-1, -1, -1):
		s += digits[i] * m
		m *= radix
	return s

solutions = {}
buildSolutionTree(solutions, cleanedInstrChunks)
# print('\nsolutions tree:', *solutions.items(), '', sep='\n\n')

digitsMax = buildBestSolution(solutions, maximizing=True)
solutionMax = numberFromList(digitsMax)
print('\nsolutionMax:', solutionMax, '\n') # 53999995829399

# ------------------------------------------
# Part 2:

digitsMin = buildBestSolution(solutions, maximizing=False)
solutionMin = numberFromList(digitsMin)
print('\nsolutionMin:', solutionMin, '\n') # 11721151118175

# Runtime: 1.2s in total.

exit()

# ------------------------------------------

# What follows isn't used at all, indeed the program given as input is not to be executed ;)

posMap = { 'w' : 0, 'x' : 1, 'y' : 2, 'z' : 3 }

def run(instructions, posMap, inputs):
	states, inputsIdx = [0] * 4, 0
	for instr in instructions:
		entry = instr.split(' ')
		if entry[0] == 'inp':
			if inputsIdx >= len(inputs):
				print('Not enough inputs given!')
				exit()
			states[posMap[entry[1]]] = int(inputs[inputsIdx])
			inputsIdx += 1
			continue
		value = states[posMap[entry[2]]] if entry[2] in posMap else int(entry[2])
		if entry[0] == 'add':
			states[posMap[entry[1]]] += value
		elif entry[0] == 'mul':
			states[posMap[entry[1]]] *= value
		elif entry[0] == 'div':
			if value == 0:
				print('Using <div> with 0!')
				exit()
			states[posMap[entry[1]]] //= value
		elif entry[0] == 'mod':
			if states[posMap[entry[1]]] < 0 or value <= 0:
				print('Using <mod> with (%d, %d)!' % (states[posMap[entry[1]]], value))
				exit()
			states[posMap[entry[1]]] = states[posMap[entry[1]]] % value
		else: # 'eq'
			states[posMap[entry[1]]] = int(states[posMap[entry[1]]] == value)
	return states

model = '13579246899999'
states = run(instructions, posMap, list(model))
print('\nmodel:', model, '->', states)

# This is way too slow:
def findLargestModelNumber(instructions, posMap):
	inputs, n = [9] * 14, len(inputs)
	while True:
		while inputs[n-1] >= 0:
			print(inputs)
			if not 0 in inputs:
				states = run(instructions, posMap, inputs)
				if states[3] == 0:
					return inputs
			inputs[n-1] -= 1
		left = n - 2
		while left >= 0 and inputs[left] == 0:
			left -= 1
		if left < 0:
			print('No solution found.')
			return []
		inputs[left] -= 1
		for i in range(left+1, n):
			inputs[i] = 9

# solution = findLargestModelNumber(instructions, posMap)
# print('\nBest solution:', solution)
