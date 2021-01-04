import itertools
import functools

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_19"
# filename = "resources/example_19_2"
filename = "resources/input_19"

lines = get_lines(filename)

def format_rule(line):
	i = line.find(':')
	index = int(line[ : i])
	if line[i+2] == '\"':
		return index, line[i+3 : -1]
	else:
		splitted = line[i+2 : ].split('|')
		splitted = list(map(lambda s : s.split(' '), splitted))
		splitted = list(map(lambda s : list(filter(lambda s : s != '', s)), splitted))
		splitted = list(map(lambda s : list(map(lambda s : int(s), s)), splitted))
		return index, splitted

# print(format_rule("72: \"b\""))
# print(format_rule("10: 113 108"))
# print(format_rule("71: 72 106 | 52 128"))
# print(format_rule("0: 4 1 5"))
# print(format_rule("8: 42"))

def get_rules_msg(lines):
	rules, messages = [], []
	rules_mode = True
	for line in lines:
		if line == '':
			rules_mode = False
			continue
		elif rules_mode == True:
			rules.append(format_rule(line))
		else:
			messages.append(line)
	return rules, messages

rules, messages = get_rules_msg(lines)
rules = sorted(rules, key=lambda c : c[0]) # sorted by index - unnecessary.
# print("rules:", rules, "\nmessages:", messages, "\n")

def create_rules_map(rules):
	max_index = max(rules, key=lambda c : c[0]) # works even if 'rules' is unsorted.
	rules_map = [0] * (max_index[0] + 1)
	for index in range(len(rules_map)):
		rules_map[index] = []
	return rules_map

def can_be_known(rules_map, rule):
	for r in rule:
		for index in r:
			if rules_map[index] == []:
				return False
	return True

def generate_strings(rules_map, rule):
	new_strings = []
	for bloc in rule:
		new_strings_list = list(map(lambda i : rules_map[i] , bloc))
		cartesian_product = list(itertools.product(*new_strings_list))
		concatenation = lambda strings : functools.reduce(lambda str1, str2 : str1 + str2, strings)
		new_strings += list(map(concatenation, cartesian_product))
	# return list(set(new_strings)) # slow and useless, no redundancies!
	return new_strings

def fill_rules_map(rules, rules_map):
	unknown_number = len(rules) # len(rules) <= len(rules_map) in general!
	while unknown_number > 0:
		for r in rules:
			index, rule = r
			if rules_map[index] == []:
				if type(rule) == str:
					rules_map[index] = [rule] # single string
					unknown_number -= 1
				elif can_be_known(rules_map, rule):
					rules_map[index] = generate_strings(rules_map, rule)
					unknown_number -= 1

rules_map = create_rules_map(rules)
fill_rules_map(rules, rules_map)
# print("rules_map:", rules_map, "\n") # ok!

key_size = len(rules_map[0][0]) # same length in all rules_map[0] !!!
print("rules_map[0]: len =", len(rules_map[0]), ", key_size =", key_size)

# faster with size test:
invalid_messages = list(filter(lambda msg : not (len(msg) == key_size and msg in rules_map[0]), messages))
result = len(messages) - len(invalid_messages)
print("\nresult:", result)


print("\nPart 2:\n")

# 8: 42 | 42 8
# 11: 42 31 | 42 11 31
# 0: 8 11

def gen_new_rule(bound):
	new_rule = []
	for i in range(1, bound):
		for j in range(i+1, bound):
			r = [42] * j + [31] * i
			new_rule.append(r)
	return new_rule

max_msg_len = len(max(messages, key=len))
min_chunk_size = min(len(rules_map[42][0]), len(rules_map[31][0]))
bound = max_msg_len // min_chunk_size
print("max_msg_len:", max_msg_len, ", min_chunk_size:", min_chunk_size, ", bound:", bound)

new_rule = gen_new_rule(bound)
# print(new_rule)

def check_string(rules_map, new_rule, string):
	for bloc in new_rule:
		start, fits = 0, True
		for index in bloc:
			size = len(rules_map[index][0])
			fits = string[start : start + size] in rules_map[index]
			start += size
			if fits == False:
				break
		if fits == True and len(string) == start:
			# print("Fits with:", bloc)
			return True
	return False

def count_new_valid_msg(invalid_messages):
	count = 0
	for msg in invalid_messages:
		if check_string(rules_map, new_rule, msg):
			count += 1
	return count

result += count_new_valid_msg(invalid_messages)
print("\nresult:", result)
