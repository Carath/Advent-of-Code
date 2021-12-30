def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

inputData = getFileLines('resources/input_02.txt')
inputData = [ s.split(' ') for s in inputData if s != '' ]
# print(inputData)

def computePos(data):
	horiz, depth = 0, 0
	for d in data:
		direc, val = d
		val = int(val)
		if direc == 'forward':
			horiz += val
		elif direc == 'down':
			depth += val
		else: # up
			depth -= val
	return horiz, depth

horiz, depth = computePos(inputData)
print('horiz: %d, depth: %d' % (horiz, depth))
result = horiz * depth
print('Result:', result) # 2187380

# ------------------------------------------
# Part 2:

def computePosAndAim(data):
	horiz, depth, aim = 0, 0, 0
	for d in data:
		direc, val = d
		val = int(val)
		if direc == 'forward':
			horiz += val
			depth += aim * val
		elif direc == 'down':
			aim += val
		else: # up
			aim -= val
	return horiz, depth, aim

horiz, depth, aim = computePosAndAim(inputData)
print('horiz: %d, depth: %d, aim: %d' % (horiz, depth, aim))
result = horiz * depth
print('Result 2:', result) # 2086357770
