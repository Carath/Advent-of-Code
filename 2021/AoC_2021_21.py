# Careful, players take turns. Thus draws cannot happen, since player 1 wins first.

# start_1, start_2 = 4, 8 # example
start_1, start_2 = 7, 1

def deterministicGame(pos_1, pos_2, winningScore=1000):
	score_1, score_2, rolls, shift = 0, 0, 0, 6
	while True:
		rolls += 3
		if rolls % 2 == 1:
			pos_1 = (pos_1 - 1 + shift) % 10 + 1
			score_1 += pos_1
			if score_1 >= winningScore:
				break # stopping immediately!
		else:
			pos_2 = (pos_2 - 1 + shift) % 10 + 1
			score_2 += pos_2
			if score_2 >= winningScore:
				break
		shift += 9
	return min(score_1, score_2), rolls

loserScore, dieRolls = deterministicGame(start_1, start_2)
print('Result:', loserScore * dieRolls, '\n') # 684495

# ------------------------------------------
# Part 2:

def fillOutcomeCounts(outcomeCounts, dieValues, rollsNumber, outcomeSum=0):
	if rollsNumber <= 0:
		if not outcomeSum in outcomeCounts:
			outcomeCounts[outcomeSum] = 0
		outcomeCounts[outcomeSum] += 1
		return
	for outcome in dieValues:
		fillOutcomeCounts(outcomeCounts, dieValues, rollsNumber - 1, outcomeSum + outcome)

def expand(board, outcomeCounts, newUniversesMap, winCounts, winningScore, currUniverse, wannabeUniverse, universeCount, player):
	score, pos = currUniverse[2 * player], currUniverse[2 * player + 1]
	for outcome in outcomeCounts:
		newPos = (pos + outcome) % len(board)
		newScore = score + board[newPos]
		newUniverseCount = universeCount * outcomeCounts[outcome]
		if newScore >= winningScore:
			winCounts[player] += newUniverseCount
			continue
		newUniverse = (*wannabeUniverse, newScore, newPos)
		if player >= len(winCounts) - 1:
			if not newUniverse in newUniversesMap:
				newUniversesMap[newUniverse] = 0
			newUniversesMap[newUniverse] += newUniverseCount
			continue
		expand(board, outcomeCounts, newUniversesMap, winCounts, winningScore, currUniverse, newUniverse, newUniverseCount, player+1)

# There will be as many players as starting values.
# Memoization is used here since the current state of any universe is determined by the score
# and position of its players, thus only a finite number of states are possible for each universe:
# ((winningScore + 1) * len(board)) ^ len(startingValues) = 48400 for the given parameters.
def quantumGame(startingValues, board=list(range(1, 11)), dieValues=[1, 2, 3], rollsNumber=3, winningScore=21):
	assert startingValues != [], 'There must be at least one player.'
	for value in startingValues:
		assert value in board, 'Invalid starting value: %d vs %s' % (value, str(board))
	outcomeCounts = {}
	fillOutcomeCounts(outcomeCounts, dieValues, rollsNumber)
	print('outcomes sum -> count:', *outcomeCounts.items(), '', sep='\n')
	winCounts, firstUniverse = [0] * len(startingValues), []
	for value in startingValues:
		firstUniverse.extend([0, board.index(value)]) # score, pos
	universesMap = { tuple(firstUniverse) : 1 } # universe state -> count
	while universesMap != {}:
		newUniversesMap = {}
		for universe in universesMap:
			expand(board, outcomeCounts, newUniversesMap, winCounts, winningScore, universe, (), universesMap[universe], 0)
		universesMap = newUniversesMap
	return winCounts

winCounts = quantumGame([start_1, start_2])
print('Found:', winCounts)
print('\nResult:', max(winCounts)) # 152587196649184 in 0.3s
