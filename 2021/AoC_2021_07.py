import math

def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def findBestPos(values, cost):
	xmin, xmax = min(values), max(values)
	bestPos, minSum = 0, math.inf
	for pos in range(xmin, xmax+1):
		currSum = sum([ cost(abs(val - pos)) for val in values ])
		if currSum < minSum:
			minSum = currSum
			bestPos = pos
	return bestPos, minSum

cost_1 = lambda step : step

# inputData = '16,1,2,0,4,2,7,1,2,14'
inputData = getFileLines('resources/input_07.txt')[0]
inputData = [ int(s) for s in inputData.split(',') ]
# print(inputData)

result = findBestPos(inputData, cost_1)
print('Result:', result[1]) # 343441

# ------------------------------------------
# Part 2:

cost_2 = lambda step : step * (step+1) // 2

result = findBestPos(inputData, cost_2)
print('Result:', result[1]) # 98925151
