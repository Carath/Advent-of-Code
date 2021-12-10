def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def getInput(string):
	return list(map(int, string.split(',')))

# program modifies itself!
def run(program):
	program = program[:] # copying, preventing side effects!
	i = 0
	while i < len(program):
		opcode = program[i]
		if opcode == 99:
			# print('Quitting (opcode 99)')
			break
		if i + 4 > len(program):
			print('Not enough values at rank %d!' % i)
			break
		src1 = program[i+1]
		src2 = program[i+2]
		dest = program[i+3]
		if opcode == 1:
			program[dest] = program[src1] + program[src2]
		elif opcode == 2:
			program[dest] = program[src1] * program[src2]
		else:
			print('Invalid opcode', opcode)
		i += 4
	if i >= len(program):
		print('No instructions left, stopping.')
	return program

# stringInput = '1,0,0,0,99' # becomes 2,0,0,0,99 (1 + 1 = 2).
# stringInput = '2,3,0,3,99' # becomes 2,3,0,6,99 (3 * 2 = 6).
# stringInput = '2,4,4,5,99,0' # becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
# stringInput = '1,1,1,4,99,5,6,0,99' # becomes 30,1,1,4,2,5,6,0,99.

inputFile = 'resources/input_02.txt'
stringInput = getFileLines(inputFile)[0]
print(stringInput, '\n')

program = getInput(stringInput)

# Fixing old program:
program[1] = 12
program[2] = 2

result = run(program)
print('Result 1:', result[0], '\n')

# ------------------------------------------
# Part 2:

def findParams(program, target):
	for pos1 in range(100):
		for pos2 in range(100):
			program[1] = pos1
			program[2] = pos2
			result = run(program)
			if result[0] == target:
				print('Found target for params:', pos1, pos2)
				return pos1, pos2
	print('Target not found!')
	return -1, -1

noun, verb = findParams(program, 19690720)
result = 100 * noun + verb
print('Result 2:', result)
