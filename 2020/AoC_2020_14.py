# import time

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_14"
filename = "resources/input_14"

lines = get_lines(filename)
# print(lines)

def get_values(s):
	i, j, k = s.index("["), s.index("]"), s.index("=")
	return int(s[i+1 : j]), int(s[k+1 : ])

def get_chunks(lines):
	chunks, chunk = [], []
	for line in lines:
		if line[0 : 4] == "mask":
			if chunk != []:
				chunks.append(chunk)
				chunk = []
			offset = line.index("=")
			mask = line[offset+2 : ]
			chunk.append(mask)
		else:
			mem_values = get_values(line)
			chunk.append(mem_values)
	chunks.append(chunk)
	return chunks

chunks = get_chunks(lines)
# print(chunks)

def do_mask(mask, value): # careful! this is not an AND mask!
	res, exponent = 0, 1
	for i in range(len(mask) - 1, -1, -1): # in {n-1, ..., 0}
		if mask[i] == 'X':
			res += (value % 2) * exponent
		else:
			res += int(mask[i]) * exponent
		value //= 2
		exponent *= 2
	return res

# print(do_mask(chunks[0][0], 11)) # ok
# print(do_mask(chunks[0][0], 101)) # ok
# print(do_mask(chunks[0][0], 0)) # ok

def get_mem_state(chunks):
	hash_map = [0] * 99999 # hardcoded
	for chunk in chunks:
		mask, mem_values = chunk[0], chunk[1 : ]
		for (index, value) in mem_values:
			hash_map[index] = do_mask(mask, value)
	# print(hash_map)
	sum_mem = 0
	for value in hash_map:
		sum_mem += value
	return sum_mem

print("result:", get_mem_state(chunks))


print("\nPart 2:\n")

def get_addresses(mask, index):
	addresses = [0]
	exponent = 1
	for i in range(len(mask) - 1, -1, -1): # in {n-1, ..., 0}
		if mask[i] == 'X':
			new_addresses = addresses.copy() # to prevent an infinite loop!
			for address in addresses:
				new_addresses.append(address + exponent)
			addresses = new_addresses
		else:
			offset = (int(mask[i]) | (index % 2)) * exponent
			for j in range(len(addresses)):
				addresses[j] += offset
		index //= 2
		exponent *= 2
	return addresses

print(get_addresses("000000000000000000000000000000X1001X", 42)) # ok

# N.B: cannot use a hash map here: too much addresses!
def get_mem_state_2(chunks):
	# start = time.time_ns()
	values_at_address = []
	for chunk in chunks:
		mask, mem_values = chunk[0], chunk[1 : ]
		for (index, value) in mem_values:
			addresses = get_addresses(mask, index)
			for address in addresses:
				values_at_address.append((address, value))
	values_at_address.sort(key=lambda c : c[0]) # sorting by address
	# print(values_at_address)
	current_address, sum_mem = values_at_address[0][0], 0
	for i in range(1, len(values_at_address)):
		if values_at_address[i][0] != current_address:
			sum_mem += values_at_address[i - 1][1]
			current_address = values_at_address[i][0]
	sum_mem += values_at_address[len(values_at_address) - 1][1]
	# elapsed = (time.time_ns() - start) / 1e9
	# print("Time:", elapsed, "s")
	return sum_mem

# Do not run this on the example, for it will be too slow!
# This works on the actual input because there is few 'X' in each masks...
print("\nresult:", get_mem_state_2(chunks))
