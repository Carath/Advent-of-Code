def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def countIncreases(data):
	count = 0
	for i in range(1, len(data)):
		count += int(data[i] > data[i-1])
	return count

inputData = getFileLines('resources/input_01.txt')
inputData = list(map(int, inputData))
# print(inputData)

result = countIncreases(inputData)
print('Result:', result) # 1655

# ------------------------------------------
# Part 2:

threeMeasurement = lambda data, i : data[i] + data[i+1] + data[i+2]

def countThreeMeasurement(data):
	count = 0
	for i in range(1, len(data)-2):
		count += int(threeMeasurement(data, i) > threeMeasurement(data, i-1))
	return count

result = countThreeMeasurement(inputData)
print('Result 2:', result) # 1683
