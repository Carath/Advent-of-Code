def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def evolve(population, days):
	populationMap = { key : 0 for key in range(9) }
	for fish in population:
		populationMap[fish] += 1
	for day in range(days):
		# print('day %d:' % day, populationMap)
		dividingFishes = populationMap[0]
		for key in range(8):
			populationMap[key] = populationMap[key+1]
		populationMap[6] += dividingFishes
		populationMap[8] = dividingFishes
	# print('day %d:' % (day+1), populationMap)
	return sum(populationMap[key] for key in populationMap)

inputData = getFileLines('resources/input_06.txt')
inputData = inputData[0].split(',')
inputData = [ int(s) for s in inputData ]
print('Input:', inputData, '\n')

# result = evolve_2([3, 4, 3, 1, 2], 18)
# result = evolve_2([3, 4, 3, 1, 2], 80)
result = evolve(inputData, 80)
print('\nResult:', result, '\n') # 353079

# ------------------------------------------
# Part 2:

result = evolve(inputData, 256)
print('\nResult:', result) # 1605400130036
