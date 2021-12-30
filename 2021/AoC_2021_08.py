def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

# inputData = ['acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf']
# inputData = getFileLines('resources/example_08.txt')
inputData = getFileLines('resources/input_08.txt')

inputData = [ s.split(' | ') for s in inputData ]
inputData = [ [ c.split(' ') for c in line ] for line in inputData ]
# print(*inputData, sep='\n')

def getLengthMap(signalDigits):
	lengthMap = { length : [] for length in range(2, 8) }
	for s in signalDigits:
		lengthMap[len(s)].append(set(s))
	return lengthMap

def countEasyOnes(entries):
	theSum = 0
	for entry in entries:
		signalDigits, outputs = entry
		lengthMap = getLengthMap(signalDigits)
		for output in outputs:
			candidates = lengthMap[len(output)]
			if len(candidates) == 1:
				theSum += 1
	return theSum

print('\nResult:', countEasyOnes(inputData), '\n') # 512

# ------------------------------------------
# Part 2:

# Using structure found on the correct segments display:
def findTranslation(signalDigits):
	lengthMap = getLengthMap(signalDigits)
	translationMap = { digit : set() for digit in range(10) }
	translationMap[1] = lengthMap[2][0]
	translationMap[7] = lengthMap[3][0]
	translationMap[4] = lengthMap[4][0]
	translationMap[8] = lengthMap[7][0]
	chunk = translationMap[4].union(translationMap[7])
	for candidate in lengthMap[6]:
		if chunk.issubset(candidate):
			translationMap[9] = candidate
		elif translationMap[1].issubset(candidate):
			translationMap[0] = candidate
		else:
			translationMap[6] = candidate
	for candidate in lengthMap[5]:
		if translationMap[1].issubset(candidate):
			translationMap[3] = candidate
		elif len(candidate.intersection(translationMap[6])) == 4:
			translationMap[2] = candidate
		else:
			translationMap[5] = candidate
	return translationMap

def retrieveDigits(translationMap, outputs):
	theSum = 0
	for output in outputs:
		outputSet = set(output)
		for digit in translationMap:
			if translationMap[digit] == outputSet:
				# print("Output '%s' -> digit %d" % (output, digit))
				theSum = theSum * 10 + digit
				break
	return theSum

def computeSum(entries):
	theSum = 0
	for entry in entries:
		translationMap = findTranslation(entry[0])
		theSum += retrieveDigits(translationMap, entry[1])
	return theSum

result = computeSum(inputData)
print('\nResult:', result) # 1091165
