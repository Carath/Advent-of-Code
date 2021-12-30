# Problem characteristics:
# - Lots of global path possibilities.
# - Relatively small number of possible states.
# - A state entirely defines its successors, no matter the previous states (state has no memory),
#   same with the costs for going from said state to its successors. However the lowest cost
#   of a given state depends on the path taken to reach this state.
# - Successors (potentially distant) of a state cannot go back to said state (no cycle).

# Main algorithm works by memoization of visited states: current lowest cost and direct successors are saved:
# - When a state is visited for the first time, its current cost is saved and all its successors
#   are recursively visited too, until the end state or a deadlock is reached.
# - When a state is revisited, its successors are not, but if the current cost of that state is lower
#   than the saved one, then said state cost is updated with the new one, and all of its successors cost
#   must be recursively checked for update.
# - Update of a (distant) successor: given a state Si with updated cost Ci, and a direct successor Sj
#   with current cost Cj (= Ck + Ckj from a direct predecessor Sk of Sj, Sk != Si a priori),
#   then the updated cost of Sj is: min(Cj, Ci + Cij).

# Constants:
targetColMap = { 'A' : 3, 'B' : 5, 'C' : 7, 'D' : 9 }
charCostMap = { 'A' : 1, 'B' : 10, 'C' : 100, 'D' : 1000 }
waintingTiles = [(1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 11)]
print('waintingTiles:', waintingTiles)

def printGrid(grid, cost=0):
	lines = [ ''.join(row) for row in grid ]
	lines[0] += ' (cost: %d)' % cost
	print('', *lines, '', sep='\n')

# Careful, in all that follows agents must be sorted to have a unique representation.
def getAgents(grid):
	agents = []
	for row in range(len(grid)):
		for col in range(len(grid[row])):
			char = grid[row][col]
			if char in targetColMap:
				agents.append((char, row, col))
	# Removing already parked agents from the list. They will still be stored in the grid!
	for char in targetColMap:
		col = targetColMap[char]
		for row in range(len(grid)-2, 1, -1):
			if grid[row][col] != char:
				break
			agents.remove((char, row, col))
	agents.sort()
	return agents

def canDepart(grid, row, col):
	for r in range(row-1, 1, -1):
		if grid[r][col] != '.':
			return False
	return True

def findSpot(grid, char):
	targetCol = targetColMap[char]
	for r in range(len(grid)-2, 1, -1):
		if grid[r][targetCol] == '.': # above tiles must be empty
			return (r, targetCol)
		if grid[r][targetCol] != char:
			break
	return None

# Checks if the path isn't blocked too:
def getPathLength(grid, start, end):
	step = 1 if end[1] > start[1] else -1
	for col in range(start[1]+step, end[1]+step, step):
		if grid[1][col] != '.':
			return -1
	return abs(start[0] - end[0]) + abs(start[1] - end[1]) # manhattan distance

# A further potential optimization could be done: preventing simple deadlocks.
def visitStates(statesMap, grid, waintingTiles, agents):
	# Careful! Do _not_ discard states with current best cost greater than the current greater cost of the final
	# state. Indeed, both quantities may change over time, so (almost) every valid state should be explored.
	for agentIdx in range(len(agents)):
		char, row, col = agents[agentIdx]
		if row == 1: # on a waiting tile
			freeRoomTile = findSpot(grid, char)
			if freeRoomTile != None:
				generateNewState(grid, agents, agentIdx, char, (row, col), freeRoomTile, True)
		elif canDepart(grid, row, col): # still at starting position
			freeRoomTile = findSpot(grid, char) # trying to park the agent if possible, to explore less states.
			if freeRoomTile != None:
				generateNewState(grid, agents, agentIdx, char, (row, col), freeRoomTile, True, stopover=(1, col))
			else:
				for tile in waintingTiles:
					if grid[tile[0]][tile[1]] == '.':
						generateNewState(grid, agents, agentIdx, char, (row, col), tile, False)

def generateNewState(grid, agents, agentIdx, char, coord, targetTile, agentParked, stopover=None):
	start = coord if stopover == None else stopover
	pathLength = getPathLength(grid, start, targetTile)
	if pathLength < 0:
		return
	if stopover != None:
		pathLength += coord[0] - 1
	newAgents = agents[:]
	if agentParked:
		newAgents.pop(agentIdx) # this one's done.
	else:
		newAgents[agentIdx] = (char, targetTile[0], targetTile[1])
	newAgents.sort() # guaranteeing a unique representation.
	if stateRegistered(statesMap, agents, newAgents, charCostMap[char] * pathLength):
		return
	newGrid = [ row[:] for row in grid ]
	newGrid[coord[0]][coord[1]] = '.'
	newGrid[targetTile[0]][targetTile[1]] = char
	visitStates(statesMap, newGrid, waintingTiles, newAgents)

# Memoizing visited states:
def stateRegistered(statesMap, agents, newAgents, moveCost):
	currKey, nextKey = tuple(agents), tuple(newAgents)
	# marking the next state as successor of the current one:
	currSuccessors = statesMap[currKey][1]
	if nextKey not in currSuccessors:
		currSuccessors[nextKey] = moveCost
	# Saving or updating state cost:
	newCost =  statesMap[currKey][0] + moveCost
	if nextKey in statesMap:
		if newCost < statesMap[nextKey][0]:
			statesMap[nextKey][0] = newCost
			updateCosts(statesMap, nextKey)
		return True # already seen state, not exploring it again.
	statesMap[nextKey] = [newCost, {}] # cost, successor -> move cost map
	return False # must be explored.

# Cannot loop infinitely: agents cannot step back!
# Careful, nodes need to be visited by all paths.
def updateCosts(statesMap, key):
	for nextKey in statesMap[key][1]:
		newCost = statesMap[key][0] + statesMap[key][1][nextKey]
		if newCost < statesMap[nextKey][0]:
			statesMap[nextKey][0] = newCost
			updateCosts(statesMap, nextKey)

def buildAbestPath(statesMap, path=[]):
	if path == []:
		assert () in statesMap, 'Final state has never been reached!'
		path = [(statesMap[()][0], ())] # final state
	currKey, predCostKey = path[-1][1], None
	for key in statesMap:
		if currKey in statesMap[key][1]:
			predCost = statesMap[key][0]
			moveCost = statesMap[key][1][currKey]
			currCost = statesMap[currKey][0]
			if predCost + moveCost == currCost:
				predCostKey = (predCost, key)
				break
	if predCostKey == None:
		path.reverse()
		return path
	path.append(predCostKey)
	return buildAbestPath(statesMap, path)


# inputData = '''
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########
# ''' # example 1 - 12521

inputData = '''
#############
#...........#
###D#A#D#C###
  #B#C#B#A#
  #########
''' # input 1 - 14348

grid = [ list(s) for s in inputData.split('\n') if s != '' ]
printGrid(grid)

agents = getAgents(grid)
statesMap = { tuple(agents) : [0, {}] }
visitStates(statesMap, grid, waintingTiles, agents)

path = buildAbestPath(statesMap)
print('Path:', *path, sep='\n')

print('\nBest cost:', statesMap[()][0], '\n') # 14348

# ------------------------------------------
# Part 2:

# inputData = '''
# #############
# #...........#
# ###B#C#B#D###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
# ''' # example 2 - 44169

inputData = '''
#############
#...........#
###D#A#D#C###
  #D#C#B#A#
  #D#B#A#C#
  #B#C#B#A#
  #########
''' # input 2 - 40954

grid = [ list(s) for s in inputData.split('\n') if s != '' ]
printGrid(grid)

agents = getAgents(grid)
statesMap = { tuple(agents) : [0, {}] }
visitStates(statesMap, grid, waintingTiles, agents)

print('Best cost:', statesMap[()][0]) # 40954

# Took 2.8s in total
