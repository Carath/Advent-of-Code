def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

def getData(string):
	blocs = string.split('\n\n')
	drawnNumbers = [ int(s) for s in blocs[0].split(',') ]
	blocs = [ bloc.split('\n') for bloc in blocs[1:] ]
	blocs = [ list(filter(lambda s : s != '', bloc)) for bloc in blocs ] # for trailing newlines at the end.
	blocs = [ [ list(filter(lambda s : s != '', row.split(' '))) for row in bloc ] for bloc in blocs ]
	boardsMatrixList = [ [ [ int(s) for s in row ] for row in bloc ] for bloc in blocs ]
	size = len(boardsMatrixList[0][0])
	return size, drawnNumbers, boardsMatrixList

def getBoardMaps(boardsMatrixList):
	boardMaps = []
	for i in range(len(boardsMatrixList)):
		boardMatrix = boardsMatrixList[i]
		boardMap = {}
		boardMaps.append(boardMap)
		for row in range(len(boardMatrix)):
			for col in range(len(boardMatrix[0])):
				val = boardMatrix[row][col]
				boardMap[val] = [row, col, 0]
	return boardMaps

def addValue(board, val):
	if val in board:
		board[val][2] = 1
		return True
	return False

def checkBoard(board, size):
	rowsSums, colsSums = [0] * size, [0] * size
	for val in board:
		if board[val][2] == 1:
			row, col = board[val][0], board[val][1]
			rowsSums[row] += 1
			colsSums[col] += 1
	return size in rowsSums or size in colsSums

def getScore(board, lastVal):
	s = 0
	for val in board:
		if board[val][2] == 0:
			s += val
	return lastVal * s

def playForWin(drawnNumbers, boardMaps, size):
	for val in drawnNumbers:
		for i in range(len(boardMaps)):
			if addValue(boardMaps[i], val) and checkBoard(boardMaps[i], size):
				print('Winning board %d!' % i)
				return getScore(boardMaps[i], val)
	print('No winner yet...')
	return -1

stringInput = getFileContent('resources/input_04.txt')
size, drawnNumbers, boardsMatrixList = getData(stringInput)
print('size:', size)
print('drawnNumbers:\n', drawnNumbers)
print('boards matrices:', *boardsMatrixList, sep='\n')

boardMaps = getBoardMaps(boardsMatrixList)
# print('boardMaps:', *boardMaps, sep='\n')

score = playForWin(drawnNumbers, boardMaps, size)
print('score:', score, '\n') # 44088

# ------------------------------------------
# Part 2:

def playForLoss(drawnNumbers, boardMaps, size):
	boardMapsIndexes = range(len(boardMaps))
	for val in drawnNumbers:
		nextBoardMapsIndexes = []
		for i in boardMapsIndexes:
			if addValue(boardMaps[i], val) and checkBoard(boardMaps[i], size):
				lastWinIndex = i
				# print('Winning board °%d, discarding it!' % i)
			else:
				nextBoardMapsIndexes.append(i)
		boardMapsIndexes = nextBoardMapsIndexes
		if nextBoardMapsIndexes == []:
			print('Last board °%d won!' % lastWinIndex)
			return getScore(boardMaps[lastWinIndex], val)
	print('No winner yet...')
	return -1

score = playForLoss(drawnNumbers, boardMaps, size)
print('score:', score) # 23670
