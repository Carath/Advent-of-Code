def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def getInput(string):
	return list(map(int, string.split(',')))

def readValue(program, val, mode):
	return val if mode == 1 else program[val]

# program modifies itself!
def run(program, inputs):
	program = program[:] # copying, preventing side effects!
	i, j = 0, 0
	outputs = []
	while i < len(program):
		opcode, params = program[i] % 100, program[i] // 100
		param1, param2 = params % 10, params // 10
		# print('opcode: %d, param 1: %d, param 2: %d' % (opcode, param1, param2))
		if opcode == 99:
			# print('Quitting (opcode 99)')
			break
		try:
			if opcode in [3, 4]:
				instrSize = 2
				dest = program[i+1]
			elif opcode in [5, 6]:
				instrSize = 3
				val1 = readValue(program, program[i+1], param1)
				val2 = readValue(program, program[i+2], param2)
			else:
				instrSize = 4
				val1 = readValue(program, program[i+1], param1)
				val2 = readValue(program, program[i+2], param2)
				dest = program[i+3] # writing only, mode 0 forced.
		except:
			print('Not enough values at rank %d!' % i)
			break
		if opcode == 1: # sum
			program[dest] = val1 + val2
		elif opcode == 2: # product
			program[dest] = val1 * val2
		elif opcode == 3: # writing input
			if j >= len(inputs):
				print('Missing an input at rank %d!' % i)
				break
			# print('j: %d, dest index: %d' % (j, dest))
			program[dest] = inputs[j]
			j += 1
		elif opcode == 4: # saving output
			outputs.append(readValue(program, dest, param1))
		elif opcode == 5: # jump if true
			if val1 != 0:
				i = val2 - instrSize
		elif opcode == 6: # jump if false
			if val1 == 0:
				i = val2 - instrSize
		elif opcode == 7: # less than
			program[dest] = int(val1 < val2)
		elif opcode == 8: # equals
			program[dest] = int(val1 == val2)
		else:
			print('Invalid opcode', opcode)
		i += instrSize
	if i >= len(program):
		print('No instructions left, stopping.')
	return program, outputs

# stringInput = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'

inputFile = 'resources/input_05.txt'
stringInput = getFileLines(inputFile)[0]
print(stringInput, '\n')
program = getInput(stringInput)

newProg, outputs = run(program, [1])
print('Result 1:', outputs) # 0s and 13087969

# ------------------------------------------
# Part 2:

newProg, outputs = run(program, [5])
print('Result 2:', outputs) # 14110739
