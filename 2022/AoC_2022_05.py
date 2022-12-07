def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_05.txt"
path = "resources/input_05.txt"

lines = [ s for s in getFileContent(path).split("\n") if s != "" ]

stacksNumber = (len(lines[0])+1)//4
print("stacksNumber:", stacksNumber)
stacks, instructions = [ [] for i in range(stacksNumber) ], []
for line in lines:
	if "[" in line:
		row = [ line[i:i+4] for i in range(0, len(line), 4) ]
		for i in range(stacksNumber):
			if "[" in row[i]:
				stacks[i] += row[i][1:2]
	elif "move" in line:
		splitted = line.split(" ")
		instructions.append([ int(splitted[i]) for i in [1, 3, 5] ])

print("\nstacks:", *stacks, sep="\n")
print("\ninstructions:", *instructions, sep="\n")

def moveCrates(stacks, instructions, reverseCrates):
	stacks = stacks[:] # preventing side effects
	for instr in instructions:
		number, i, j = instr[0], instr[1]-1, instr[2]-1
		chunk = stacks[i][:number][::-1] if reverseCrates else stacks[i][:number]
		stacks[j] = chunk + stacks[j]
		stacks[i] = stacks[i][number:]
	return stacks

movedStacks = moveCrates(stacks, instructions, True)
print("\nMoved stacks:", *movedStacks, sep="\n")

result = "".join([ movedStacks[i][0] for i in range(stacksNumber) ])
print("\nResult:", result, "\n") # VQZNJMWTR

# # ------------------------------------------
# # Part 2:

movedStacks = moveCrates(stacks, instructions, False)
print("\nMoved stacks:", *movedStacks, sep="\n")

result = "".join([ movedStacks[i][0] for i in range(stacksNumber) ])
print("\nResult 2:", result) # NLCDCLVMQ
