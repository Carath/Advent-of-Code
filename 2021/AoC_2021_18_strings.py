def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# direction: -1 for left, 1 for right.
# Returns (-1, -1) on failure.
def findClosest(string, offset, direction):
	i = offset + direction
	while i in range(len(string)) and string[i] in ['[', ']', ',']:
		i += direction
	j = i + direction
	while j in range(len(string)) and not string[j] in ['[', ']', ',']:
		j += direction
	start, end = min(i, j-direction), max(i, j-direction)+1
	subString = string[start : end]
	# print('subString:', subString)
	if subString == '':
		return None, -1, -1
	return int(subString), start, end

def findExplosion(string):
	count, start, end = 0, -1, -1
	for i in range(len(string)):
		if string[i] == '[':
			count += 1
			start = i
		if string[i] == ']':
			count -= 1
			if count >= 4:
				end = i + 1
				break
	return start, end

def doExplosion(string):
	start, end = findExplosion(string)
	if start == -1 or end == -1:
		# print('Nothing to explode.')
		return False, string
	valuesStr = string[start+1 : end-1].split(',')
	leftValue, rightValue = int(valuesStr[0]), int(valuesStr[1])
	leftClosest, leftStart, leftEnd = findClosest(string, start, -1)
	rightClosest, rightStart, rightEnd = findClosest(string, end, 1)
	leftString, rightString = string[:start], string[end:]
	if leftClosest != None:
		leftString = string[:leftStart] + str(leftClosest + leftValue) + string[leftEnd:start]
	if rightClosest != None:
		rightString = string[end:rightStart] + str(rightClosest + rightValue) + string[rightEnd:]
	string = leftString + '0' + rightString
	return True, string

def findAndDoSplit(string):
	start = 0
	while start in range(len(string)):
		rightClosest, start, end = findClosest(string, start, 1)
		if rightClosest != None and rightClosest >= 10:
			a, b = rightClosest // 2, rightClosest - rightClosest // 2
			string = string[:start] + '[%d,%d]' % (a, b) + string[end:]
			return True, string
	# print('Nothing to split.')
	return False, string

def reduceString(string):
	status = True
	while status:
		explosionStatus = True
		while explosionStatus:
			explosionStatus, string = doExplosion(string)
		status, string = findAndDoSplit(string)
	return string

def getClosingIdx(string, start):
	assert string != '' and string[0] == '[', 'Invalid string: %s' % string
	count = 0
	for i in range(start, len(string)):
		if string[i] == '[':
			count += 1
		elif string[i] == ']':
			count -= 1
			if count == 0:
				return i + 1
	return -1

def computeMagnitude(string):
	assert string != '', 'Empty string!'
	if string[0] == '[':
		idx = getClosingIdx(string, 1) if string[1] == '[' else string.find(',')
		assert idx != -1, 'Invalid string: %s' % string
		return 3 * computeMagnitude(string[1:idx]) + 2 * computeMagnitude(string[idx+1:-1])
	return int(string)

def sumLines(lines):
	string = lines[0]
	for line in lines[1:]:
		string = '[%s,%s]' % (string, line)
		string = reduceString(string) # must be done after each sum!
	return string


# inputData = getFileContent('resources/example_18.txt')
inputData = getFileContent('resources/input_18.txt')

lines = [ line for line in inputData.split('\n') if line != '' ]

string = sumLines(lines)
print('Sum of inputs:', string)

magnitude = computeMagnitude(string)
print('\nMagnitude:', magnitude) # 3892

# ------------------------------------------
# Part 2:

# Testing all i != j, since 'addition' isn't commutative:
def getMaxMagnitude(lines):
	maxMagnitude = 0
	for i in range(len(lines)):
		for j in range(len(lines)):
			if i == j:
				continue
			string = '[%s,%s]' % (lines[i], lines[j])
			string = reduceString(string) # must be done after each sum!
			maxMagnitude = max(maxMagnitude, computeMagnitude(string))
	return maxMagnitude

maxMagnitude = getMaxMagnitude(lines)
print('\nMax magnitude:', maxMagnitude) # 4909 in 4.6 sec
