print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

def count_chars(char, string):
	sum = 0
	for i in range(0, len(string)):
		if string[i] == char:
			sum += 1
	return sum

result = count_chars('a', "abcde")
print(result)


def is_password_valid(min, max, char, string):
	count = count_chars(char, string)
	return min <= count and count <= max

result = is_password_valid(1, 3, 'a', "abcde")
print(result)


def parse(string):
	i, j, k = string.index("-"), string.index(" "), string.index(":")
	return int(string[0 : i]), int(string[i+1 : j]), string[j+1 : k], string[k+2 : ]

print(parse("1-3 a: abcde"))


def count_number_of_valid(lines):
	count = 0
	for line in lines:
		min, max, char, string = parse(line)
		if is_password_valid(min, max, char, string):
			count += 1
	return count

lines = get_lines("resources/input_2")

result = count_number_of_valid(lines)
print("\nresult", result)


print("\nPart 2:\n")

def is_password_valid_2(min, max, char, string):
	return (string[min] == char) != (string[max] == char) # xor

def count_number_of_valid_2(lines):
	count = 0
	for line in lines:
		min, max, char, string = parse(line)
		if is_password_valid_2(min-1, max-1, char, string):
			count += 1
	return count

result = count_number_of_valid_2(lines)
print("result", result)
