print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_16"
filename = "resources/input_16"

lines = get_lines(filename)
# print(lines)

def get_ranges(line):
	i, j = line.index(":"), line.index(" or")
	s1, s2 = line[i+2 : j], line[j+4 : ]
	k, l = s1.index("-"), s2.index("-")
	return (int(s1[0 : k]), int(s1[k+1 : ])), (int(s2[0 : l]), int(s2[l+1 : ]))

def get_fields(line):
	return list(map(lambda n : int(n), line.split(",")))

def get_data(lines):
	ranges, myticket, nearby_tickets = [], [], []
	i, phase = 0, 0
	while i < len(lines):
		line = lines[i]
		if line == "":
			phase += 1
			i += 1 # skipping next line
		elif phase == 0:
			ranges.append(get_ranges(line))
		elif phase == 1:
			myticket = get_fields(line)
		else:
			nearby_tickets.append(get_fields(line))
			# nearby_tickets.extend(get_fields(line))
		i += 1
	return ranges, myticket, nearby_tickets

ranges, myticket, nearby_tickets = get_data(lines)
# print(ranges, "\n")
# print(myticket, "\n")
# print(nearby_tickets, "\n")

def check_validity(ranges, myticket, nearby_tickets):
	invalid_values, valid_tickets = [], [myticket]
	for ticket in nearby_tickets:
		ticket_validity = True
		for value in ticket:
			value_fits = False
			for r in ranges:
				(a, b), (c, d) = r
				if value in range(a, b+1) or value in range(c, d+1):
					value_fits = True
					break
			if value_fits == False:
				invalid_values.append(value)
				ticket_validity = False
		if ticket_validity == True:
			valid_tickets.append(ticket)
	return invalid_values, valid_tickets

invalid_values, valid_tickets = check_validity(ranges, myticket, nearby_tickets)
print("invalid_values (w/ repeat):\n\n", invalid_values)
print("\nresult:", sum(invalid_values))


print("\nPart 2:\n")

# print("valid_tickets:")
# for ticket in valid_tickets:
	# print(ticket)
print("valid tickets number:", len(valid_tickets))

def get_valid_values(valid_tickets):
	valid_values = []
	for ticket in valid_tickets:
		valid_values += ticket
	print("valid values number (w/ repeat):", len(valid_values))
	valid_values = list(set(valid_values)) # removing duplicates
	valid_values = sorted(valid_values)
	print("valid values number:", len(valid_values), "\n")
	return valid_values

valid_values = get_valid_values(valid_tickets)
# print(valid_values)

def get_invalid_ranges(ranges, value):
	invalid_ranges = []
	for r in ranges:
		(a, b), (c, d) = r
		if not (value in range(a, b+1) or value in range(c, d+1)):
			invalid_ranges.append(r)
	return invalid_ranges

invalid_list = list(map(lambda v : (v, get_invalid_ranges(ranges, v)), valid_values))


def print_list(list_of_list):
	for l in list_of_list:
		print(l)
	print()

# sub optimal.
# len(myticket) = len(ranges)
def create_truth_map(ranges, invalid_list):
	truth_map = []
	for i in range(len(ranges)):
		index_list = list(range(len(ranges))) # new copy
		truth_map.append((i, index_list))
		# print(truth_map[i])
	for ticket in valid_tickets:
		for value_index in range(len(ranges)):
			value = ticket[value_index]
			j = 0
			while invalid_list[j][0] != value:
				j += 1
			inv_rg_list = invalid_list[j][1]
			for rg in inv_rg_list:
				rg_index = ranges.index(rg)
				try:
					truth_map[rg_index][1].remove(value_index)
				except Exception:
					pass
	return truth_map

truth_map = create_truth_map(ranges, invalid_list)
truth_map = sorted(truth_map, key=lambda c : len(c[1]))
print_list(truth_map)

def find_permutation(ranges):
	permutation, answer_list = [-1] * len(ranges), []
	for i in range(0, len(ranges)):
		index, candidates = truth_map[i]
		candidates = list(filter(lambda v: v not in answer_list, candidates))
		answer = candidates[0] # should be only one here...
		permutation[index] = answer
		answer_list.append(answer)
	return permutation

permutation = find_permutation(ranges)
print(permutation)

result = 1
for i in range(6):
	result *= myticket[permutation[i]]
print("\nresult:", result) # YES!
