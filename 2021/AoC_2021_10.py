def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def isOpeningChar(char):
	return char in ['(', '[', '{', '<']

def isClosingChar(char):
	return char in [')', ']', '}', '>']

def closingChar(char):
	if char == '(':
		return ')'
	if char == '[':
		return ']'
	if char == '{':
		return '}'
	if char == '<':
		return '>'
	return '.' # default

def scoreIllegalChar(char):
	if char == ')':
		return 3
	if char == ']':
		return 57
	if char == '}':
		return 1197
	if char == '>':
		return 25137
	return 0 # default

def simplifyExpression(string):
	items, nextItems = list(enumerate(string)), []
	while True:
		i = 0
		while i < len(items):
			if i < len(items)-1 and items[i+1][1] == closingChar(items[i][1]):
				i += 2
			else:
				nextItems.append(items[i])
				i += 1
		newString = ''.join(list(map(lambda c : c[1], nextItems)))
		# print(newString)
		if len(items) <= len(nextItems):
			break
		items, nextItems = nextItems, []
	if items == []:
		print('Valid string.\n')
		return (-1, '.'), items
	else:
		closingChars = list(filter(lambda c : isClosingChar(c[1]), items))
		if closingChars == []:
			print('Incomplete string:', newString, '\n')
			return (-1, '.'), items
		else:
			print('Corrupted string:', newString, '\n')
			return closingChars[0], items

def computeIllegalCharsScore(simplifiedData):
	score = 0
	for data in simplifiedData:
		if data[0] != (-1, '.'):
			score += scoreIllegalChar(data[0][1])
	return score

# inputData = getFileLines('resources/example_10.txt')
inputData = getFileLines('resources/input_10.txt')
inputData = list(filter(lambda s : s != '', inputData))
print('\n', inputData, '\n')

simplifiedData = [ simplifyExpression(s) for s in inputData ]

score = computeIllegalCharsScore(simplifiedData)
print('Illegal chars score:', score, '\n') # 266301

# ------------------------------------------
# Part 2:

def scoreMissingChar(char):
	if char == ')':
		return 1
	if char == ']':
		return 2
	if char == '}':
		return 3
	if char == '>':
		return 4
	return 0 # default

def computeMissingCharsScore(simplifiedData):
	scoresList = []
	for data in simplifiedData:
		if data[0] == (-1, '.') and data[1] != []:
			missing = list(reversed([ closingChar(c[1]) for c in data[1] ]))
			newString = ''.join(missing)
			# print('Completing with:', newString)
			score = 0
			for char in missing:
				score = score * 5 + scoreMissingChar(char)
			scoresList.append(score)
	scoresList.sort()
	print('\nScores list:', scoresList)
	return scoresList[len(scoresList) // 2]

score = computeMissingCharsScore(simplifiedData)
print('\nMissing chars score:', score) # 3404870164
