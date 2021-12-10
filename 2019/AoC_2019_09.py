def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def getInput(string):
	return list(map(int, string.split(',')))

def readValue(program, relativeBase, val, mode):
	try:
		if mode == 0:
			return program[val]
		elif mode == 1:
			return val
		elif mode == 2:
			return program[relativeBase + val]
		else:
			print('Unsupported mode in readValue():', mode)
			exit()
	except:
		print('Out of bound access in readValue() for mode:', mode)
		exit()

def writeValue(program, relativeBase, address, val, mode):
	try:
		if mode == 0:
			program[address] = val
		elif mode == 1:
			print('Cannot use mode 1 in writeValue()!')
			exit()
		elif mode == 2:
			program[relativeBase + address] = val
		else:
			print('Unsupported mode in writeValue():', mode)
			exit()
	except:
		print('Out of bound access in writeValue() for mode:', mode)
		exit()

# Program modifies itself, but a new copy is returned!
# 2 values are returned: the outputs and the new program, unless some inputs are
# missing, in that case a third value being the current program index is returned.
def run(program, inputs, start=0):
	program = program[:] # copying, preventing side effects!
	i, relativeBase, inputIndex = start, 0, 0
	outputs = []
	while i < len(program):
		opcode, params = program[i] % 100, program[i] // 100
		param1, param2, param3 = params % 10, (params // 10) % 10, params // 100
		# print('opcode: %d, param1: %d, param2: %d, param3: %d' % (opcode, param1, param2, param3))
		if opcode == 99:
			# print('Quitting (opcode 99)')
			break
		elif opcode in [3, 4, 9]:
			instrSize = 2
			dest = program[i+1]
		elif opcode in [5, 6]:
			instrSize = 3
			val1 = readValue(program, relativeBase, program[i+1], param1)
			val2 = readValue(program, relativeBase, program[i+2], param2)
		else: # in [1, 2, 7, 8]
			instrSize = 4
			val1 = readValue(program, relativeBase, program[i+1], param1)
			val2 = readValue(program, relativeBase, program[i+2], param2)
			dest = program[i+3] # writing only, mode 0 forced.
		if opcode == 1: # sum
			writeValue(program, relativeBase, dest, val1 + val2, param3)
		elif opcode == 2: # product
			writeValue(program, relativeBase, dest, val1 * val2, param3)
		elif opcode == 3: # writing input
			if inputIndex >= len(inputs):
				# print('Missing an input at rank %d!' % i)
				return outputs, program, i # returning an additional value: the current program index.
			writeValue(program, relativeBase, dest, inputs[inputIndex], param1)
			inputIndex += 1
		elif opcode == 4: # saving output
			outputs.append(readValue(program, relativeBase, dest, param1))
		elif opcode == 5: # jump if true
			if val1 != 0:
				i = val2 - instrSize
		elif opcode == 6: # jump if false
			if val1 == 0:
				i = val2 - instrSize
		elif opcode == 7: # less than
			writeValue(program, relativeBase, dest, int(val1 < val2), param3)
		elif opcode == 8: # equals
			writeValue(program, relativeBase, dest, int(val1 == val2), param3)
		elif opcode == 9: # shift 'relativeBase'
			relativeBase += readValue(program, relativeBase, dest, param1)
		else:
			print('Invalid opcode', opcode)
			exit()
		i += instrSize
	if i >= len(program):
		print('No instructions left, stopping.')
	return outputs, program


if __name__ == '__main__':

	# stringInput = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
	# stringInput = '109,19,204,-34,99'
	# stringInput = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
	# stringInput = '1102,34915192,34915192,7,4,7,99,0'
	# stringInput = '104,1125899906842624,99'

	inputFile = 'resources/input_09.txt'
	stringInput = getFileLines(inputFile)[0]
	print(stringInput, '\n')
	program = getInput(stringInput)
	program += [0] * 1000000

	outputs = run(program, [1])[0]
	print('Outputs:', outputs) # 3429606717

	# ------------------------------------------
	# Part 2:

	outputs = run(program, [2])[0]
	print('Outputs:', outputs) # 33679
