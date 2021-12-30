def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def computeCloseness(inputData, roundUp):
	size = len(inputData[0])
	array = [ getRankBit(inputData, i, roundUp) for i in range(size) ]
	print('Found:', array)
	return arrayToRadix(array, 2)

def getRankBit(candidates, rank, roundUp):
	ithSum = sum([l[rank] for l in candidates]) / len(candidates)
	bit = 0 if ithSum < 0.5 else 1
	return bit if roundUp else 1 - bit

def arrayToRadix(array, radix):
	res, m = 0, 1
	for i in range(len(array)):
		res += m * int(array[len(array) - 1 - i])
		m *= radix
	return res

inputData = getFileLines('resources/input_03.txt')
inputData = [ [ int(c) for c in s ] for s in inputData ]
# print(inputData)

gamma = computeCloseness(inputData, True)
epsilon = computeCloseness(inputData, False)
print('gamma:', gamma, '\nepsilon:', epsilon)

result = gamma * epsilon
print('Result:', result, '\n') # 2954600

# ------------------------------------------
# Part 2:

def findCandidate(inputData, roundUp):
	candidates = inputData[:]
	size, i = len(inputData[0]), 0
	while len(candidates) >= 2 and i < size:
		bit = getRankBit(candidates, i, roundUp)
		candidates = [ l for l in candidates if l[i] == bit ]
		i += 1
	print('Found:', candidates[0])
	return arrayToRadix(candidates[0], 2)

oxygen = findCandidate(inputData, True)
CO2 = findCandidate(inputData, False)
print('oxygen:', oxygen, '\nCO2:', CO2)

lifeSupportRating = oxygen * CO2
print('Life support rating:', lifeSupportRating) # 1662846
