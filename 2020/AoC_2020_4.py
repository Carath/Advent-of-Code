print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines


def get_key_index(key):
	switcher = {
		"byr": 0,
		"iyr": 1,
		"eyr": 2,
		"hgt": 3,
		"hcl": 4,
		"ecl": 5,
		"pid": 6,
		"cid": 7,
	}
	return switcher.get(key, "Invalid key")


# passport must be filled with 0s initially.
def fill_passport_map_1(passport_map, key_data):
	i = key_data.index(":")
	key = key_data[0 : i]
	index = get_key_index(key)
	passport_map[index] = 1


def check_passport_map(passport_map):
	return passport_map == [1] * 8 or passport_map == [1, 1, 1, 1, 1, 1, 1, 0] # 'cid' ignored!


def passport_validity(passport_map):
	validity = check_passport_map(passport_map)
	# print(passport_map)
	# print(validity)
	return 1 if validity else 0


def find_1(lines):
	count = 0
	passport_map = [0] * 8
	for line in lines:
		if line == '': # passport filled.
			count += passport_validity(passport_map)
			passport_map = [0] * 8 # reset
			continue
		i, j, n = 0, 0, len(line)
		while j < n:
			if line[j] == ' ':
				s = line[i : j]
				# print(s)
				fill_passport_map_1(passport_map, s)
				i = j + 1
			j += 1
		s = line[i : j]
		# print(s)
		fill_passport_map_1(passport_map, s)
	# Last passport:
	count += passport_validity(passport_map)
	return count


# filename = "resources/example_4"
filename = "resources/input_4"
lines = get_lines(filename)
result = find_1(lines)
print("result", result)


print("\nPart 2:\n")


# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# 	If cm, the number must be at least 150 and at most 193.
# 	If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.


def get_hcl_status(value):
	if len(value) != 7 or value[0] != '#':
		return False
	for i in range(1, len(value)): # starting after '#'
		c = ord(value[i]) # ascii code
		if not (c in range(48, 58) or c in range(97, 103)): # in 0 ... 9 or a ... f
			return False
	return True


def get_pid_status(value):
	if len(value) != 9:
		return False
	for i in range(0, len(value)):
		c = ord(value[i]) # ascii code
		if not c in range(48, 58): # in 0 ... 9
			return False
	return True


def fill_passport_map_2(passport_map, key_data):
	i = key_data.index(":")
	key = key_data[0 : i]
	value = key_data[i+1 : ]
	index = get_key_index(key)

	if index == 0: # byr
		if int(value) in range(1920, 2003):
			passport_map[index] = 1

	elif index == 1: # iyr
		if int(value) in range(2010, 2021):
			passport_map[index] = 1

	elif index == 2: # eyr
		if int(value) in range(2020, 2031):
			passport_map[index] = 1

	elif index == 3: # hgt
		try:
			number, suffix = int(value[0 : -2]), value[len(value) - 2 : ]
			if (suffix == "cm" and number in range(150, 194)) or (suffix == "in" and number in range(59, 77)):
				passport_map[index] = 1
		except Exception: # number could not be casted as integer!
			pass

	elif index == 4: # hcl
		if get_hcl_status(value):
			passport_map[index] = 1

	elif index == 5: # ecl
		if value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
			passport_map[index] = 1

	elif index == 6: # pid
		if get_pid_status(value):
			passport_map[index] = 1

	else: # cid
		passport_map[index] = 1 # irrelevant.

def find_2(lines):
	count = 0
	passport_map = [0] * 8
	for line in lines:
		if line == '': # passport filled.
			count += passport_validity(passport_map)
			passport_map = [0] * 8 # reset
			continue
		i, j, n = 0, 0, len(line)
		while j < n:
			if line[j] == ' ':
				s = line[i : j]
				# print(s)
				fill_passport_map_2(passport_map, s)
				i = j + 1
			j += 1
		s = line[i : j]
		# print(s)
		fill_passport_map_2(passport_map, s)
	# Last passport:
	count += passport_validity(passport_map)
	return count


# filename = "resources/example_4_invalid"
# filename = "resources/example_4_valid"
filename = "resources/input_4"
lines = get_lines(filename)
result = find_2(lines)
print("result", result)
