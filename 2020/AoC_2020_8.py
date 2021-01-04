print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_8"
filename = "resources/input_8"

lines = get_lines(filename)

format_value = lambda c : (c[0], int(c[1]))
instructions = list(map(format_value, map(lambda line : line.split(" "), lines)))
# print(instructions)

def follow_instructions(instructions):
	n, acc, i = len(instructions), 0, 0
	hash_map = [0] * n
	while i < n and hash_map[i] == 0:
		hash_map[i] += 1
		cmd, value = instructions[i]
		if cmd == "jmp":
			i += value
			continue
		elif cmd == "acc":
			acc += value
		# case cmd == "nop": do nothing.
		i += 1
	return acc, i == n

result = follow_instructions(instructions)
print("result: " + str(result))


print("\nPart 2:\n")

def find_instr_to_change(instructions):
	for j in range(0, len(instructions)):
		cmd, value = instructions[j]
		if cmd == "acc": # nothing to change here
			continue
		elif cmd == "jmp":
			instructions[j] = "nop", value
		else: # cmd == "nop":
			instructions[j] = "jmp", value
		acc, status = follow_instructions(instructions)
		# print(instructions) # including the change
		instructions[j] = cmd, value # reset
		if status == True:
			return acc

result = find_instr_to_change(instructions)
print("result: " + str(result))
